"""Component to create switch groups with shared states"""
import logging
from collections import OrderedDict

from homeassistant.const import EVENT_STATE_CHANGED, STATE_ON
from homeassistant.core import HomeAssistant, Event, State
from tests.components.switch.common import turn_on, turn_off

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'switch_group'


def setup(hass: HomeAssistant, config: OrderedDict) -> bool:
    groups: OrderedDict = config[DOMAIN]
    devices_map = {}

    # Map groups
    for group in groups.keys():
        for entity_id in groups[group]:
            if entity_id not in devices_map:
                devices_map[entity_id] = []

            devices_map[entity_id].append(group)

    def on_state_change(event: Event):
        entity_id = event.data.get('entity_id')
        new_state: State = event.data.get('new_state')

        if entity_id in devices_map:
            groups_to_fire = devices_map[entity_id]
            for group_to_fire in groups_to_fire:
                for device_to_fire in groups[group_to_fire]:
                    current_state = hass.states.get(device_to_fire)

                    if current_state is not None and current_state.state != new_state.state:
                        if new_state.state == STATE_ON:
                            turn_on(hass, device_to_fire)
                        else:
                            turn_off(hass, device_to_fire)

    hass.bus.listen(EVENT_STATE_CHANGED, on_state_change)
    return True
