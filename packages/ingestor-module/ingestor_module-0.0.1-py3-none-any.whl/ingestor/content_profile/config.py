from ingestor.common.constants import AGE_RATING, CONTENT_ID, TITLE, CREATED_ON, YEAR, STATUS, DURATION_MINUTE, IS_GEO_BLOCK, \
    IS_FREE, IS_ORIGINAL, IS_BRANDED, IS_EXCLUSIVE, SYNOPSIS_BH, SYNOPSIS_EN, START_DATE, END_DATE, MODIFIED_ON, TYPE, \
    CATEGORY, SUB_CAT_BH, SUB_CAT_EN, TAG_NAME, TAG_DESCRIPTION, ACTOR_NAME, \
    SEASON_NAME, CONTENT_CORE_ID, CONTENT_CORE_EPISODE, CONTENT_CORE_TITLE, CONTENT_CORE_SYNOPSIS, \
    CONTENT_CORE_SYNOPSIS_EN, PRODUCT_NAME_EN, \
    PRODUCT_NAME, PRODUCT_CREATED_ON, PACKAGE_NAME_BH, PACKAGE_IS_PAY_TV, PACKAGE_CREATED_ON, \
    CLUSTER_CATEGORY_ID, CLUSTER_CATEGORY_TITLE_BH, CLUSTER_CATEGORY_TITLE_EN, TAG_ID, COUNTRY_DESCRIPTION, HOMEPAGE_ID, \
    HOMEPAGE_TITLE, HOMEPAGE_TITLE_EN, HOMEPAGE_STATUS, HOMEPAGE_TYPE, HOMEPAGE_CREATED_ON, HOMEPAGE_MODIFIED_ON

'''DEFINING NODE PROPERTIES'''


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
                     TYPE: property_value[TYPE]}
    return node_property


def rating_node_properties(property_value):
    node_property = {AGE_RATING: property_value[AGE_RATING]}
    return node_property


def category_node_properties(property_value):
    node_property = {CATEGORY: property_value[CATEGORY]}
    return node_property


def subcategory_node_properties(property_value):
    node_property = {SUB_CAT_BH: property_value[SUB_CAT_BH],
                     SUB_CAT_EN: property_value[SUB_CAT_EN]}
    return node_property


def country_node_properties(property_value):
    node_property = {COUNTRY_DESCRIPTION: property_value[COUNTRY_DESCRIPTION]}
    return node_property


def tag_node_properties(property_value):
    node_property = {TAG_NAME: property_value[TAG_NAME],
                     TAG_DESCRIPTION: property_value[TAG_DESCRIPTION],
                     TAG_ID: property_value[TAG_ID]}
    return node_property


def actor_node_properties(property_value):
    node_property = {ACTOR_NAME: property_value[ACTOR_NAME]}
    return node_property


def season_node_properties(property_value):
    node_property = {SEASON_NAME: property_value[SEASON_NAME]}
    return node_property


def content_episode_node_properties(property_value):
    node_property = {CONTENT_CORE_ID: property_value[CONTENT_CORE_ID],
                     CONTENT_CORE_EPISODE: property_value[CONTENT_CORE_EPISODE],
                     CONTENT_CORE_TITLE: property_value[CONTENT_CORE_TITLE],
                     CONTENT_CORE_SYNOPSIS: property_value[CONTENT_CORE_SYNOPSIS],
                     CONTENT_CORE_SYNOPSIS_EN: property_value[CONTENT_CORE_SYNOPSIS_EN]}
    return node_property


def product_node_properties(property_value):
    node_property = {PRODUCT_NAME_EN: property_value[PRODUCT_NAME_EN],
                     PRODUCT_NAME: property_value[PRODUCT_NAME],
                     PRODUCT_CREATED_ON: property_value[PRODUCT_CREATED_ON]}
    return node_property


def package_node_properties(property_value):
    node_property = {PACKAGE_NAME_BH: property_value[PACKAGE_NAME_BH],
                     PACKAGE_IS_PAY_TV: property_value[PACKAGE_IS_PAY_TV],
                     PACKAGE_CREATED_ON: property_value[PACKAGE_CREATED_ON]}
    return node_property


def cluster_category_properties(property_value):
    node_property = {CLUSTER_CATEGORY_ID: property_value[CLUSTER_CATEGORY_ID],
                     CLUSTER_CATEGORY_TITLE_BH: property_value[CLUSTER_CATEGORY_TITLE_BH],
                     CLUSTER_CATEGORY_TITLE_EN: property_value[CLUSTER_CATEGORY_TITLE_EN]}
    return node_property


def homepage_node_properties(property_value):
    node_property = {HOMEPAGE_ID: property_value[CLUSTER_CATEGORY_ID],
                     HOMEPAGE_TITLE: property_value[CLUSTER_CATEGORY_TITLE_BH],
                     HOMEPAGE_TITLE_EN: property_value[CLUSTER_CATEGORY_TITLE_EN],
                     HOMEPAGE_STATUS: property_value[HOMEPAGE_STATUS],
                     HOMEPAGE_TYPE: property_value[HOMEPAGE_TYPE],
                     HOMEPAGE_CREATED_ON: property_value[HOMEPAGE_CREATED_ON],
                     HOMEPAGE_MODIFIED_ON: property_value[HOMEPAGE_MODIFIED_ON]}
    return node_property


'''DEFINING RELATIONSHIP NAMES'''
HAS_DURATION = "HAS_DURATION"
HAS_RATING = "HAS_RATING"
HAS_CATEGORY = "HAS_CATEGORY"
HAS_SUBCATEGORY = "HAS_SUBCATEGORY"
HAS_COUNTRY = "HAS_COUNTRY"
HAS_TAG = "HAS_TAG"
HAS_ACTOR = "HAS_ACTOR"
HAS_SEASON = "HAS_SEASON"
HAS_EPISODE = "HAS_EPISODE"
HAS_PRODUCT = "HAS_PRODUCT"
HAS_PACKAGE = "HAS_PACKAGE"
HAS_CONTENT = "HAS_CONTENT"
HAS_CLUSTER_CATEGORY = "HAS_CLUSTER_CATEGORY"
HAS_HOMEPAGE = "HAS_HOMEPAGE"
