from ingestor.common.constants import AGE_RATING, CONTENT_ID, TITLE, CREATED_ON, YEAR, STATUS, DURATION_MINUTE, \
    IS_GEO_BLOCK, IS_FREE, IS_ORIGINAL, IS_BRANDED, IS_EXCLUSIVE, SYNOPSIS_BH, SYNOPSIS_EN, START_DATE, END_DATE, \
    MODIFIED_ON, TYPE


# Content Node Properties

def content_node_properties(property_value):
    node_property = {CONTENT_ID: property_value[CONTENT_ID],
                     TITLE: property_value[TITLE],
                     CREATED_ON: property_value[CREATED_ON],
                     YEAR: property_value[YEAR],
                     STATUS: property_value[STATUS],
                     DURATION_MINUTE: property_value[DURATION_MINUTE],
                     IS_GEO_BLOCK: property_value[IS_GEO_BLOCK],
                     IS_FREE: property_value[IS_FREE],
                     IS_ORIGINAL: property_value[IS_ORIGINAL],
                     IS_BRANDED: property_value[IS_BRANDED],
                     IS_EXCLUSIVE: property_value[IS_EXCLUSIVE],
                     SYNOPSIS_BH: property_value[SYNOPSIS_BH],
                     SYNOPSIS_EN: property_value[SYNOPSIS_EN],
                     START_DATE: property_value[START_DATE],
                     END_DATE: property_value[END_DATE],
                     MODIFIED_ON: property_value[MODIFIED_ON],
                     TYPE: property_value[TYPE],
                     AGE_RATING: property_value[AGE_RATING]}
    return node_property


'''DEFINING RELATIONSHIP NAMES'''
HAS_CATEGORY = "HAS_CATEGORY"
HAS_SUBCATEGORY = "HAS_SUBCATEGORY"
HAS_COUNTRY = "HAS_COUNTRY"
HAS_TAG = "HAS_TAG"
HAS_ACTOR = "HAS_ACTOR"
HAS_CONTENT_CORE = "HAS_CONTENT_CORE"
HAS_PRODUCT = "HAS_PRODUCT"
HAS_PACKAGE = "HAS_PACKAGE"
HAS_HOMEPAGE = "HAS_HOMEPAGE"
