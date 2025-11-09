from plugin import Plugin

import pandas as pd
import ast
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from numpy import ptp

class Corr_Model(Plugin):
    
    def __init__(self, rebalance):

        self.dow30 = ["AAPL","AMZN","AXP","BA","CAT","CRM","CSCO","CVX","DIS","GS","HD","HON","IBM","JNJ","JPM","MCD","MRK","MSFT","NKE","NVDA","PG","TRV","UNH","V","VZ","WMT","KO","AMGN","3M","SHW"]

        self.rebalance = rebalance

        df = pd.read_csv('/Users/gabri/Classes/Research/BacktestSys/rels_cleaned.csv')

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['timestamp'] = df['timestamp'].dt.tz_localize(None)

        cutoff_date = self.rebalance.date - pd.Timedelta(days=126)
        end_date = self.rebalance.date

        df = df[(df['timestamp'] >= cutoff_date) & (df['timestamp'] <= end_date)]

        df['original_raw'] = df['original_raw'].apply(ast.literal_eval)

        self.df = df

        returns = self.rebalance.rebalance_prices.pct_change().dropna()

        valid_assets = [asset for asset in self.dow30 if asset in returns.columns]

        self.returns = returns[valid_assets].dropna(axis=1, how='any')

        corr_matrix = self.returns.corr()

        self.D = np.sqrt(1 - corr_matrix)
        
        #print(self.D)
        tickers = self.D.index.tolist()
    
        self.G = nx.Graph()
    
        self.G.add_nodes_from(tickers)
        
        threshold = 0.80

        for i, t1 in enumerate(tickers):
            for j, t2 in enumerate(tickers):
                if i >= j: 
                    continue
                dist = self.D.iloc[i, j]
                if threshold is not None and dist < threshold:
                    continue
                self.G.add_edge(t1, t2, weight=dist)
        self.balance_graph()

        if threshold is not None:
            edges_to_remove = [(u, v) for u, v, d in self.G.edges(data=True) if d['weight'] < threshold]
            self.G.remove_edges_from(edges_to_remove)

        # plt.figure(figsize=(8, 6))
        # pos = nx.spring_layout(self.G)  # Layout para posicionamento dos nós
        # nx.draw(self.G, pos, with_labels=True, node_size=700, font_size=12)
        # plt.title("Grafo de mercado")
        # plt.show()

        # aaa

        try:
            self.degrees = dict(self.G.degree(weight='weight'))
            self.betweeness = nx.betweenness_centrality(self.G, weight='weight')
            self.closeness = nx.closeness_centrality(self.G, distance='weight')
            self.eigenvector = nx.eigenvector_centrality(self.G, weight='weight', max_iter=1000)
        except Exception as e:
            print(f"Error calculating centrality measures: {e}")
        

        invest = []
        sorted_items = sorted(self.degrees.items(), key=lambda item: item[1])
        count = 0
        for key, _ in sorted_items:
            if key not in invest:
                invest.append(key)
                count += 1
            if count >= 3:
                break

        sorted_items = sorted(self.betweeness.items(), key=lambda item: item[1])
        count = 0
        for key, _ in sorted_items:
            if key not in invest:
                invest.append(key)
                count += 1
            if count >= 3:
                break

        sorted_items = sorted(self.closeness.items(), key=lambda item: item[1])
        count = 0
        for key, _ in sorted_items:
            if key not in invest:
                invest.append(key)
                count += 1
            if count >= 3:
                break

        sorted_items = sorted(self.eigenvector.items(), key=lambda item: item[1])
        count = 0
        for key, _ in sorted_items:
            if key not in invest:
                invest.append(key)
                count += 1
            if count >= 3:
                break

        highlight_nodes = set(invest)

        print("Nós destacados:", highlight_nodes)

        pos = nx.spring_layout(self.G, weight='weight', seed=42)

        vals = np.array([self.eigenvector.get(n, 0.0) for n in self.G.nodes()])
        spread = np.ptp(vals) 
        node_sizes = np.full(len(vals), 300.0)
    
        node_color_map = ["crimson" if n in highlight_nodes else "#1f77b4" for n in self.G.nodes()]

        edge_weights = [
            max(0.4, float(data.get("weight", 0.0)) * 2.0)
            for _, _, data in self.G.edges(data=True)
        ]

        fig, ax = plt.subplots(figsize=(10, 7))
        nx.draw_networkx_edges(self.G, pos, ax=ax, width=edge_weights, alpha=0.6)
        nx.draw_networkx_nodes(self.G, pos, node_size=node_sizes,
                            node_color=node_color_map, edgecolors="k", linewidths=0.8)

        labels = {n: n for n in highlight_nodes}
        nx.draw_networkx_labels(self.G, pos, labels=labels, font_size=10, font_weight="bold", ax=ax)

        legend = mpatches.Patch(color="crimson")
        ax.legend(handles=[legend], loc="upper right")

        ax.set_title("Grafo — nós entre os 3 menores em qualquer métrica de centralidade", fontsize=14)
        ax.axis("off")
        plt.tight_layout()
        plt.show()


    def get_lowest_n(self, d, n=3):
        return dict(sorted(d.items(), key=lambda item: item[1])[:n])
    

    def balance_graph(self):

        try:
            for tuple in self.df['original_raw']:
                source = tuple[0]
                target = tuple[2]
                relation = tuple[1]
                if source in self.G.nodes and target in self.G.nodes:
                    if self.G.has_edge(source, target):
                        if relation == 'Positive_Impact_On':
                            self.G[source][target]['weight'] /= 2
                        elif relation == 'Negative_Impact_On':
                            self.G[source][target]['weight'] *= 2
                    else:
                        self.G.add_edge(source, target, weight=1.0)
        except Exception as e:
            print(f"Error balancing graph: {e}")


    def get_weights(self):

        invest = []

        sorted_items = sorted(self.degrees.items(), key=lambda item: item[1])
        count = 0
        for key, _ in sorted_items:
            if key not in invest:
                invest.append(key)
                count += 1
            if count >= 3:
                break

        sorted_items = sorted(self.betweeness.items(), key=lambda item: item[1])
        count = 0
        for key, _ in sorted_items:
            if key not in invest:
                invest.append(key)
                count += 1
            if count >= 3:
                break

        sorted_items = sorted(self.closeness.items(), key=lambda item: item[1])
        count = 0
        for key, _ in sorted_items:
            if key not in invest:
                invest.append(key)
                count += 1
            if count >= 3:
                break

        sorted_items = sorted(self.eigenvector.items(), key=lambda item: item[1])
        count = 0
        for key, _ in sorted_items:
            if key not in invest:
                invest.append(key)
                count += 1
            if count >= 3:
                break

        print(f'Investing in: {invest}')
        return {asset: (1/len(invest) if asset in invest else 0) for asset in self.rebalance.assets}

