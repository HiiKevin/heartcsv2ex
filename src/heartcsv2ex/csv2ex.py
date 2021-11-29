from opencmiss.zinc.context import Context
from opencmiss.zinc.field import FieldGroup

from opencmiss.utils.zinc.field import create_field_coordinates, find_or_create_field_group
from opencmiss.utils.zinc.general import create_node as create_zinc_node
from opencmiss.utils.zinc.general import ChangeManager


def write_ex(file_name, data):
    context = Context("BiV Heart Data")
    region = context.getDefaultRegion()
    load(region, data)
    region.writeFile(file_name)


def load(region, data):
    field_module = region.getFieldmodule()
    create_field_coordinates(field_module)

    for surface, points in data.items():
        node_identifiers = create_nodes(field_module, points)
        create_group_nodes(field_module, surface, node_identifiers, node_set_name='datapoints')


def create_nodes(field_module, embedded_lists, node_set_name='datapoints'):
    node_identifiers = []
    for pt in embedded_lists:
        if isinstance(pt, list):
            node_ids = create_nodes(field_module, pt, node_set_name=node_set_name)
            node_identifiers.extend(node_ids)
        else:
            local_node_id = create_zinc_node(field_module, pt, node_set_name=node_set_name)
            node_identifiers.append(local_node_id)

    return node_identifiers


def create_group_nodes(field_module, group_name, node_ids, node_set_name='nodes'):
    with ChangeManager(field_module):
        group = find_or_create_field_group(field_module, name=group_name)
        group.setSubelementHandlingMode(FieldGroup.SUBELEMENT_HANDLING_MODE_FULL)

        nodeset = field_module.findNodesetByName(node_set_name)
        node_group = group.getFieldNodeGroup(nodeset)
        if not node_group.isValid():
            node_group = group.createFieldNodeGroup(nodeset)

        nodeset_group = node_group.getNodesetGroup()
        for group_node_id in node_ids:
            node = nodeset.findNodeByIdentifier(group_node_id)
            nodeset_group.addNode(node)
