from typing import List, Any, ClassVar

from graphdb.connection import GraphDbConnection
from graphdb.graph import GraphDb
from graphdb.schema import Node
from pandas import DataFrame

from ingestor.common.constants import STATIC_NW_CATEGORY_FIELDS, \
    CAT_EN, STATIC_NW_SUBCATEGORY_FIELDS, \
    STATIC_NW_CLUSTERCATEGORY_FIELDS, NAME_LABEL, \
    STATIC_NW_TAGS_FIELDS, DESCRIPTION_LABEL, COUNTRY_NAME_LABEL, \
    STATIC_NW_COUNTRY_FIELDS, STATIC_NW_ACTOR_FIELDS, \
    STATIC_NW_PAYTVPROVIDER_FIELDS, STATIC_NW_PRODUCT_FIELDS, \
    NAME_EN_LABEL, STATIC_NW_PACKAGE_FIELDS, SUBCATEGORY_EN_LABEL, LABEL, PROPERTIES, \
    STATIC_NW_HOMEPAGE_FIELDS, TITLE_EN_LABEL, STATIC_NW_SEASON_FIELDS, SEASON_NAME_LABEL
from ingestor.common.preprocessing_utils import Utils
from ingestor.user_profile.constants import DEFAULT_NAN, DEFAULT_NUM


class StaticNodeGenerator(Utils):

    def __init__(
            self,
            data: DataFrame,
            label: str,
            graph_connection_class: GraphDbConnection
    ):
        """
        Accept the dataframe such that each
        record represents a node of label
        passed as input and each column is
        it's property

        :param data: dataframe object pandas
        :param label: node label for all
        records in input df
        """
        self.data = data
        self.node_label = label
        self.graph = GraphDb.from_connection(
            graph_connection_class
        )

    @classmethod
    def new_connection(
            cls,
            data: DataFrame,
            label: str,
            connection_uri: str
    ) -> ClassVar:
        """Initialize new connection to current class
        :param data: dataframe object pandas
        :param label: node label for all
        :param connection_uri: string connection uri
        :return: current object
        """
        return cls(data, label,
                   GraphDbConnection.from_uri(connection_uri))

    def filter_properties(
            self,
            to_keep: List
    ):
        """
        Filters the input dataframe to keep only
        the specified fields

        :param to_keep: list of attributes
        to proceed with
        :return: None, simply updates the
        instance data member
        """
        self.data = self.data[to_keep]

    def preprocess_property(
            self,
            node_property: str,
            node_default_val: Any
    ) -> bool:
        """
        Preprocess the passed node property
        using the common preprocessing script

        :param node_property: dataframe field name
        :param node_default_val: default value to
        assign in case of missing or NaN/nan values
        :return: None, simply updates the instance
        data member field values
        """
        if node_property \
                not in self.data.columns:
            return False

        self.data = \
            self.fillna_and_cast_lower(
                data=self.data,
                feature=node_property,
                default_val=node_default_val
            )

        return True

    def search_existing_network(
            self,
            prop_key: str,
            record: dict
    ) -> list:
        """
        Search the existing network to confirm
        whether the node we wish to add already
        exists or not. The search is done on a
        single key node property
        :param prop_key: Key Property
        :param record: Key property: value pair
        :return: list of nodes returned as
        search result
        """
        node_to_search = Node(
            **{
                LABEL: self.node_label,
                PROPERTIES: {
                    prop_key: record[prop_key]
                }
            }
        )
        return self.graph.find_node(node_to_search)

    def dump_nodes(
            self,
            prop_key: str
    ) -> bool:
        """
        Dump the dataframe records as
        individual nodes into GraphDB
        :return: Dumped nodes
        """
        nodes = []
        for record in self.data.to_dict(
                orient="records"):
            node = Node(
                **{
                    LABEL: self.node_label,
                    PROPERTIES: record
                })
            existing_nodes = \
                self.search_existing_network(
                    prop_key=prop_key,
                    record=record
                )
            if len(existing_nodes) > 0:
                self.graph.replace_node_property(
                    node=existing_nodes[0],
                    update_query=record
                )
                continue
            nodes.append(node)

        # create multi nodes
        self.graph.create_multi_node(nodes)
        return True

    def category_controller(
            self,
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating category nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_CATEGORY_FIELDS
        )
        self.preprocess_property(
            node_property=CAT_EN,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=CAT_EN
        )
        return True

    def subcategory_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating subcategory nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_SUBCATEGORY_FIELDS
        )
        self.preprocess_property(
            node_property=SUBCATEGORY_EN_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=SUBCATEGORY_EN_LABEL
        )
        return True

    def cluster_category_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating cluster-category nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_CLUSTERCATEGORY_FIELDS
        )
        self.preprocess_property(
            node_property=NAME_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=NAME_LABEL
        )
        return True

    def homepage_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating homepage nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_HOMEPAGE_FIELDS
        )
        self.preprocess_property(
            node_property=TITLE_EN_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=TITLE_EN_LABEL
        )
        return True

    def actor_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating actor nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_ACTOR_FIELDS
        )
        self.preprocess_property(
            node_property=NAME_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=NAME_LABEL
        )
        return True

    def tags_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating tags nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_TAGS_FIELDS
        )
        self.preprocess_property(
            node_property=NAME_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=NAME_LABEL
        )
        return True

    def country_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating country nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_COUNTRY_FIELDS
        )
        self.preprocess_property(
            node_property=COUNTRY_NAME_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.preprocess_property(
            node_property=DESCRIPTION_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=COUNTRY_NAME_LABEL
        )
        return True

    def paytv_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating PayTV Provider nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_PAYTVPROVIDER_FIELDS
        )
        self.preprocess_property(
            node_property=NAME_LABEL,
            node_default_val=DEFAULT_NUM
        )
        self.dump_nodes(
            prop_key=NAME_LABEL
        )
        return True

    def product_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating product  nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_PRODUCT_FIELDS
        )
        self.preprocess_property(
            node_property=NAME_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.preprocess_property(
            node_property=NAME_EN_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=NAME_LABEL
        )
        return True

    def package_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating package nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_PACKAGE_FIELDS
        )
        self.preprocess_property(
            node_property=NAME_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.preprocess_property(
            node_property=NAME_EN_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=NAME_LABEL
        )
        return True

    def season_controller(
            self
    ) -> bool:
        """
        Driver function for preparing meta-data
        for creating package nodes
        :return: None, simply updates the
        instance data member
        """
        self.filter_properties(
            to_keep=STATIC_NW_SEASON_FIELDS
        )
        self.preprocess_property(
            node_property=SEASON_NAME_LABEL,
            node_default_val=DEFAULT_NAN
        )
        self.dump_nodes(
            prop_key=SEASON_NAME_LABEL
        )
        return True
