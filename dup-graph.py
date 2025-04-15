import pandas as pd
import matplotlib.pyplot as plt

def plot_graph(column, label, filename):
    plt.rcParams['font.family'] = 'Helvetica'
    plt.rcParams['font.size'] = 12

    file_path = "duplication-data.csv"
    df = pd.read_csv(file_path)

    token_values = [10, 30, 50, 100]

    bright_colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']

    fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(6, 2), sharex=True)

    y_positions = list(range(len(token_values)))

    for i, token_value in enumerate(token_values):
        ax = axs[i]
        subset = df[df["minimum-tokens"] == token_value].reset_index(drop=True).head(4)

        for j, row in subset.iterrows():
            ax.barh(y=0, width=row[column], height=0.8,
                    color=bright_colors[j % len(bright_colors)], alpha=0.9)

        ax.set_yticks([0])
        ax.set_yticklabels([token_value])
        ax.tick_params(axis='y', length=0)

    fig.text(0.03, 0.6, 'Minimum tokens', va='center', ha='center', rotation='vertical', fontsize=12)

    axs[-1].set_xlabel(label)

    plt.tight_layout(rect=[0.03, -0.03, 1, 1])
    plt.savefig(filename, format='pdf', transparent=True)

if __name__ == "__main__":
    plot_graph("# duplications", "Number of duplications", "output/dup_duplications.pdf")
    plot_graph("Total lines", "Total lines", "output/dup_total_lines.pdf")
    plot_graph("Total tokens", "Total tokens", "output/dup_total_tokens.pdf")
    plot_graph("Approx # bytes", "Approximate size (bytes)", "output/dup_size.pdf")