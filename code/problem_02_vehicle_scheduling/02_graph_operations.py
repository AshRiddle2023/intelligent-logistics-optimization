# -*- coding: utf-8 -*-
import networkx as nx

def create_string_points_graph(df_points):
    """
    创建可串点站点图
    """
    G = nx.Graph()
    all_sites = set()
    for _, row in df_points.iterrows():
        all_sites.add(row['站点编号1'])
        all_sites.add(row['站点编号2'])
    for site in all_sites:
        G.add_node(site)
    for _, row in df_points.iterrows():
        G.add_edge(row['站点编号1'], row['站点编号2'])
    return G

def get_string_point_sets(G):
    """
    获取可串点集合（连通分量）
    """
    return list(nx.connected_components(G))
  
