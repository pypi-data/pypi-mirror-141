from pymodaq.daq_move.utility_classes import DAQ_Move_base  # base class
from pymodaq.daq_move.utility_classes import comon_parameters, main  # common set of parameters for all actuators
from pymodaq.daq_utils.daq_utils import ThreadCommand, getLineInfo  # object used to send info back to the main thread
from easydict import EasyDict as edict  # type of dict
from zaber_motion.ascii import Connection
from zaber_motion import Units, Tools


class DAQ_Move_Zaber(DAQ_Move_base):

    # find available COM ports
    ports = Tools.list_serial_ports()
    port = 'COM5' if 'COM5' in ports else ports[0] if len(ports) > 0 else ''

    is_multiaxes = True
    _controller_units = 'mm'
    stage_names = []

    params = [{'title': 'COM Port:', 'name': 'com_port', 'type': 'list', 'limits': ports, 'value': port},
              {'title': 'Controller:', 'name': 'controller_str', 'type': 'str', 'value': ''},
              {'title': 'MultiAxes:', 'name': 'multiaxes', 'type': 'group', 'visible': is_multiaxes, 'children': [
                     {'title': 'is Multiaxes:', 'name': 'ismultiaxes', 'type': 'bool', 'value': is_multiaxes},
                     {'title': 'Status:', 'name': 'multi_status', 'type': 'list', 'value': 'Master', 'limits': ['Master', 'Slave']},
                     {'title': 'Axis:', 'name': 'axis', 'type': 'int', 'readonly': False, 'value': 1, 'default': 1},
                 ]},
              {'title': 'Stage Properties:', 'name': 'stage_properties', 'type': 'group', 'children': [
                  {'title': 'Stage Name:', 'name': 'stage_name', 'type': 'str', 'value': '', 'readonly': True},
                  {'title': 'Stage Type:', 'name': 'stage_type', 'type': 'str', 'value': '', 'readonly': True},
              ]}
              ] + comon_parameters

    # Override definition of units parameter to make it user-changeable
    index = next(i for i, item in enumerate(params) if item["name"] == "units")
    params[index]['readonly'] = False
    params[index]['type'] = 'list'

    def __init__(self, parent=None, params_state=None):

        super().__init__(parent, params_state)
        self.controller = None
        self.unit = None

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object) custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        self.status (edict): with initialization status: three fields:
            * info (str)
            * controller (object) initialized controller
            *initialized: (bool): False if initialization failed otherwise True
        """

        try:
            self.status.update(edict(info="", controller=None, initialized=False))

            # check whether this stage is controlled by a multiaxe controller (to be defined for each plugin)
            # if multiaxes then init the controller here if Master state otherwise use external controller
            if self.settings.child('multiaxes', 'ismultiaxes').value() and self.settings.child('multiaxes',
                                   'multi_status').value() == "Slave":
                if controller is None:
                    raise Exception('no controller has been defined externally while this axe is a slave one')
                else:
                    self.controller = controller
            else:  # Master stage
                device_list = Connection.open_serial_port(self.settings.child('com_port').value()).detect_devices()
                self.controller = device_list[0]

            self.settings.child('controller_str').setValue(str(self.controller))
            self.update_axis()

            self.status.info = "Zaber controller initialized"
            self.status.controller = self.controller
            self.status.initialized = True
            return self.status

        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status',[getLineInfo()+ str(e),'log']))
            self.status.info = getLineInfo()+ str(e)
            self.status.initialized = False
            return self.status

    def update_axis(self):
        axis = self.controller.get_axis(self.settings.child('multiaxes', 'axis').value())

        # Name and ID
        self.settings.child('stage_properties', 'stage_name').setValue(
            axis.peripheral_name + ' (ID:' + str(axis.peripheral_id) + ')'
        )
        # Type
        self.settings.child('stage_properties', 'stage_type').setValue(
            axis.axis_type.name
        )
        self.settings.child('units').setReadonly(False)
        if axis.axis_type.value == 1:  # LINEAR
            self.settings.child('units').setLimits(['m', 'cm', 'mm', 'µm', 'nm', 'in'])
            self.settings.child('units').setValue('mm')
            self.unit = Units.LENGTH_MILLIMETRES

        elif axis.axis_type.value == 2:  # ROTARY
            self.settings.child('units').setLimits(['deg', 'rad'])
            self.settings.child('units').setValue('deg')
            self.unit = Units.ANGLE_DEGREES

    def check_position(self):
        """Get the current position from the hardware with scaling conversion.
        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        axis = self.controller.get_axis(self.settings.child('multiaxes', 'axis').value())
        pos = axis.get_position(unit=self.unit)

        pos = self.get_position_with_scaling(pos)
        self.current_position = pos
        self.emit_status(ThreadCommand('check_position',[pos]))
        return pos


    def close(self):
        """
        Terminate the communication protocol
        """
        self.controller.connection.close()

    def commit_settings(self, param):
        """
            | Called after a param_tree_changed signal from DAQ_Move_main.
        """
        if param.name() == 'axis':
            self.update_axis()
            self.check_position()

        elif param.name() == 'units':
            axis = self.controller.get_axis(self.settings.child('multiaxes', 'axis').value())

            epsilon_native_units = axis.settings.convert_to_native_units(
                'pos', self.settings.child('epsilon').value(), self.unit)

            if param.value() == 'm':
                self.unit = Units.LENGTH_METRES
            elif param.value() == 'cm':
                self.unit = Units.LENGTH_CENTIMETRES
            elif param.value() == 'mm':
                self.unit = Units.LENGTH_MILLIMETRES
            elif param.value() == 'µm':
                self.unit = Units.LENGTH_MICROMETRES
            elif param.value() == 'nm':
                self.unit = Units.LENGTH_NANOMETRES
            elif param.value() == 'in':
                self.unit = Units.LENGTH_INCHES
            elif param.value() == 'deg':
                self.unit = Units.ANGLE_DEGREES
            elif param.value() == 'rad':
                self.unit = Units.ANGLE_RADIANS

            self.settings.child('epsilon').setValue(axis.settings.convert_from_native_units(
                'pos', epsilon_native_units, self.unit))    # Convert epsilon to new units

            self.check_position()

        else:
            pass

    def move_Abs(self, position):
        """ Move the actuator to the absolute target defined by position
        Parameters
        ----------
        position: (flaot) value of the absolute target positioning
        """
        position = self.check_bound(position)   # if user checked bounds, the defined bounds are applied here
        self.target_position = position

        position = self.set_position_with_scaling(position)  # apply scaling if the user specified one

        axis = self.controller.get_axis(self.settings.child('multiaxes', 'axis').value())
        try:
            axis.move_absolute(position, unit=self.unit)
        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [str(e)]))

        self.poll_moving()  # start a loop to poll the current actuator value and compare it with target position
        self.check_position()

    def move_Rel(self, position):
        """ Move the actuator to the relative target actuator value defined by position

        Parameters
        ----------
        position: (flaot) value of the relative target positioning
        """
        position = (self.check_bound(self.current_position + position)
                - self.current_position)
        self.target_position = position + self.current_position

        # convert the user set position to the controller position if scaling
        # has been activated by user
        position = self.set_position_with_scaling(position)
        axis = self.controller.get_axis(self.settings.child('multiaxes', 'axis').value())

        try:
            axis.move_relative(position, unit=self.unit)
        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [str(e)]))

        self.poll_moving()
        self.check_position()

    def move_Home(self):
        """
          Send the update status thread command.
            See Also
            --------
            daq_utils.ThreadCommand
        """
        axis = self.controller.get_axis(self.settings.child('multiaxes', 'axis').value())
        axis.home()
        self.check_position()
        self.emit_status(ThreadCommand('Update_Status', ['Zaber Actuator '+ self.parent.title + ' (axis '+str(self.settings.child('multiaxes', 'axis').value())+') has been homed']))


    def stop_motion(self):
        """
        Call the specific move_done function (depending on the hardware).

        See Also
        --------
        move_done
        """
        axis = self.controller.get_axis(self.settings.child('multiaxes', 'axis').value())
        axis.stop()
        self.emit_status(ThreadCommand('Update_Status', ['Stopping Zaber actuator '+ self.parent.title + ' (axis '+str(self.settings.child('multiaxes', 'axis').value())+').']))
        self.move_done()  # to let the interface know the actuator stopped


if __name__ == '__main__':
    main(__file__)
