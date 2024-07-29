import matplotlib.pyplot as plt
import seaborn as sns


# Normalize metrics by cost
def normalize_metrics_by_cost(data, metrics, cost):
    for metric in metrics:
        data[metric + ' per $'] = data[metric] / cost
    return data


# Plot sum metrics
def plot_sum_metric(data, metric, title_suffix, palette):
    if data[metric].sum() == 0:
        return None
    plt.figure(figsize=(12, 7))
    sns.barplot(data=data, x='Month', y=metric, hue='Month', estimator=sum, palette=palette, dodge=False, errorbar=None)
    title = f'Total {metric} by Month ({title_suffix})'
    plt.title(title, fontsize=20, weight='bold')
    plt.xlabel('Month', fontsize=16)
    plt.ylabel(f'{metric}', fontsize=16)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.legend([], [], frameon=False)
    plt.tight_layout()
    filename = f'Graphs/{title_suffix}_Total_{metric}.png'
    plt.savefig(filename)
    plt.close()
    return filename


# Plot normalized metrics
def plot_normalized_metric(data, metric, title_suffix, palette):
    if data[f'{metric} per $'].sum() == 0:
        return None
    plt.figure(figsize=(12, 7))
    sns.barplot(data=data, x='Month', y=f'{metric} per $', hue='Month', estimator='mean', palette=palette, dodge=False,
                errorbar=None)
    title = f'{metric} per $ by Month ({title_suffix})'
    plt.title(title, fontsize=20, weight='bold')
    plt.xlabel('Month', fontsize=16)
    plt.ylabel(f'{metric} per $', fontsize=16)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.legend([], [], frameon=False)
    plt.tight_layout()
    filename = f'Graphs/Performance/{title_suffix}_Performance_{metric}.png'
    plt.savefig(filename)
    plt.close()
    return filename
