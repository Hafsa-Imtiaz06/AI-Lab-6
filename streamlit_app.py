import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Hospital Search Visualization",
    page_icon="🏥",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title(
    "🏥 Emergency Supply Robot - Search Visualization"
)

st.write(
    """
    Select an initial location, a goal location,
    and a search algorithm. The application will
    find and visualize the solution path.
    """
)


# ==========================================
# NODES
# ==========================================

nodes = list(hospital_graph.keys())


# ==========================================
# START NODE
# ==========================================

start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)


# ==========================================
# GOAL NODE
# ==========================================

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)


# ==========================================
# ALGORITHM
# ==========================================

algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)


# ==========================================
# RUN SEARCH
# ==========================================

if st.button("Run Search"):

    # --------------------------------------
    # Run GBFS
    # --------------------------------------

    if algorithm == "GBFS":

        path, cost = gbfs(
            start,
            goal
        )

    # --------------------------------------
    # Run A*
    # --------------------------------------

    else:

        path, cost = a_star(
            start,
            goal
        )


    # ======================================
    # CHECK SOLUTION
    # ======================================

    if path is None:

        st.error(
            "No path was found between the selected nodes."
        )

    else:

        # ==================================
        # SEARCH RESULT
        # ==================================

        st.subheader("Search Result")

        st.write(
            f"**Algorithm:** {algorithm}"
        )

        st.write(
            f"**Solution Path:** "
            f"{' → '.join(path)}"
        )

        st.write(
            f"**Total Path Cost:** "
            f"{cost:.2f}"
        )


        # ==================================
        # CREATE NETWORKX GRAPH
        # ==================================

        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():

                G.add_edge(
                    node,
                    neighbor,
                    weight=weight
                )


        # Use hospital coordinates

        pos = locations


        # ==================================
        # CREATE FIGURE
        # ==================================

        fig, ax = plt.subplots(
            figsize=(12, 7)
        )


        # ==================================
        # DRAW ALL NODES
        # ==================================

        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            node_color="lightblue",
            node_size=1800
        )


        # ==================================
        # DRAW ALL EDGES
        # ==================================

        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            arrows=True,
            arrowstyle="->",
            arrowsize=20,
            edge_color="gray"
        )


        # ==================================
        # NODE LABELS
        # ==================================

        nx.draw_networkx_labels(
            G,
            pos,
            ax=ax,
            font_size=9,
            font_weight="bold"
        )


        # ==================================
        # EDGE WEIGHTS
        # ==================================

        edge_labels = nx.get_edge_attributes(
            G,
            "weight"
        )

        nx.draw_networkx_edge_labels(
            G,
            pos,
            ax=ax,
            edge_labels=edge_labels
        )


        # ==================================
        # HIGHLIGHT SOLUTION PATH
        # ==================================

        path_edges = list(
            zip(
                path,
                path[1:]
            )
        )

        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edgelist=path_edges,
            edge_color="red",
            width=4,
            arrows=True,
            arrowstyle="->",
            arrowsize=20
        )


        # ==================================
        # GRAPH TITLE
        # ==================================

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")


        # ==================================
        # DISPLAY GRAPH IN STREAMLIT
        # ==================================

        st.pyplot(fig)