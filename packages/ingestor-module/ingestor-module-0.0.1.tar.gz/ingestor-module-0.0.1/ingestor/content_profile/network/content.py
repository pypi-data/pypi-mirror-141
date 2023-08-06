from typing import ClassVar

from graphdb.connection import GraphDbConnection
from graphdb.graph import GraphDb
from graphdb.schema import Node, Relationship
from pandas import DataFrame

# LABEL NODE NAME & VARIABLE NAME
from ingestor.common.constants import LABEL, PROPERTIES, RELATIONSHIP, CONTENT, RATING, CATEGORY, SUBCATEGORY, COUNTRY, TAG, \
    ACTOR, SEASON, CONTENT_EPISODE, CLUSTER_CATEGORY, TAG_NAME, \
    SEASON_NAME, CLUSTER_CATEGORY_ID, CONTENT_CORE_ID, PRODUCT, PRODUCT_NAME, PACKAGE, \
    PACKAGE_NAME_BH, CONTENT_ID, \
    COUNTRY_DESCRIPTION, ACTOR_NAME, HOMEPAGE, HOMEPAGE_ID
# RELATIONSHIP NAME
from ingestor.content_profile.config import HAS_RATING, HAS_CATEGORY, HAS_SUBCATEGORY, HAS_COUNTRY, HAS_TAG, HAS_ACTOR, \
    HAS_SEASON, HAS_EPISODE, HAS_CLUSTER_CATEGORY, HAS_PRODUCT, \
    HAS_PACKAGE, product_node_properties, package_node_properties, \
    rating_node_properties, content_node_properties, category_node_properties, subcategory_node_properties, \
    country_node_properties, \
    tag_node_properties, actor_node_properties, season_node_properties, content_episode_node_properties, \
    cluster_category_properties, homepage_node_properties, HAS_HOMEPAGE


class ContentNetworkGenerator:

    def __init__(
            self,
            connection_uri: str
    ):
        self.graph = GraphDb.from_connection(
            GraphDbConnection.from_uri(connection_uri)
        )

    def create_content_node(self, payload: DataFrame):
        for property_num, property_val in payload.iterrows():
            content_node = None
            if property_val[CONTENT_ID] and property_val[CONTENT_ID] is not None \
                    and property_val[CONTENT_ID] != '':
                content_node_property = content_node_properties(property_val)
                content_node = Node(**{LABEL: CONTENT, PROPERTIES: content_node_property})
                self.graph.create_node(content_node)
        return content_node

    def find_create_relationship(self, label, content_node, feature, node_properties, relationship_name,
                                 payload: DataFrame):
        for property_num, property_val in payload.iterrows():
            if property_val[feature] and property_val[feature] is not None \
                    and property_val[feature] != '':
                node_property = node_properties(property_val)
                node = Node(**{LABEL: label, PROPERTIES: node_property})
                node_in_graph = self.graph.find_node(node)
                if len(node_in_graph) > 0:
                    self.graph.create_relationship_without_upsert(content_node, node_in_graph[0],
                                                                  Relationship(**{RELATIONSHIP: relationship_name}))
                else:
                    self.graph.create_node(node)
                    self.graph.create_relationship_without_upsert(content_node, node,
                                                                  Relationship(**{RELATIONSHIP: relationship_name}))
        return content_node

    def create_update_content_network(self, payload: DataFrame):
        content_node = self.create_content_node(payload=payload)
        self.find_create_relationship(label=RATING, content_node=content_node, feature=RATING,
                                      node_properties=rating_node_properties,
                                      relationship_name=HAS_RATING,
                                      payload=payload)
        print("Generating category node")
        self.find_create_relationship(label=CATEGORY, content_node=content_node, feature=CATEGORY,
                                      node_properties=category_node_properties,
                                      relationship_name=HAS_CATEGORY,
                                      payload=payload)
        print("Generating country node")
        self.find_create_relationship(label=COUNTRY, content_node=content_node,
                                      feature=COUNTRY_DESCRIPTION,
                                      node_properties=country_node_properties,
                                      relationship_name=HAS_COUNTRY,
                                      payload=payload)
        print("Generating subcategory node")
        self.find_create_relationship(label=SUBCATEGORY, content_node=content_node,
                                      feature=SUBCATEGORY,
                                      node_properties=subcategory_node_properties,
                                      relationship_name=HAS_SUBCATEGORY,
                                      payload=payload)
        print("Generating tag node")
        self.find_create_relationship(label=TAG, content_node=content_node, feature=TAG_NAME,
                                      node_properties=tag_node_properties,
                                      relationship_name=HAS_TAG,
                                      payload=payload)
        print("Generating actor node")
        self.find_create_relationship(label=ACTOR, content_node=content_node, feature=ACTOR_NAME,
                                      node_properties=actor_node_properties,
                                      relationship_name=HAS_ACTOR,
                                      payload=payload)
        print("Generating season node")
        self.find_create_relationship(label=SEASON, content_node=content_node, feature=SEASON_NAME,
                                      node_properties=season_node_properties,
                                      relationship_name=HAS_SEASON,
                                      payload=payload)
        print("Generating cluster category node")
        self.find_create_relationship(label=CLUSTER_CATEGORY, content_node=content_node,
                                      feature=CLUSTER_CATEGORY_ID,
                                      node_properties=cluster_category_properties,
                                      relationship_name=HAS_CLUSTER_CATEGORY,
                                      payload=payload)
        print("Generating content episode node")
        self.find_create_relationship(label=CONTENT_EPISODE, content_node=content_node,
                                      feature=CONTENT_CORE_ID,
                                      node_properties=content_episode_node_properties,
                                      relationship_name=HAS_EPISODE,
                                      payload=payload)
        print("Generating product node")
        self.find_create_relationship(label=PRODUCT, content_node=content_node,
                                      feature=PRODUCT_NAME,
                                      node_properties=product_node_properties,
                                      relationship_name=HAS_PRODUCT,
                                      payload=payload)
        print("Generating content episode node")
        self.find_create_relationship(label=PACKAGE, content_node=content_node,
                                      feature=PACKAGE_NAME_BH,
                                      node_properties=package_node_properties,
                                      relationship_name=HAS_PACKAGE,
                                      payload=payload)
        print("Generating homepage node")
        self.find_create_relationship(label=HOMEPAGE, content_node=content_node,
                                      feature=HOMEPAGE_ID,
                                      node_properties=homepage_node_properties,
                                      relationship_name=HAS_HOMEPAGE,
                                      payload=payload)
        print("Done")

    @classmethod
    def from_connection_uri(
            cls,
            connection_uri: str
    ) -> ClassVar:
        """Create new object based on connection uri
        :param connection_uri: string connection uri
        :return: object class
        """
        return cls(connection_uri)

