import matplotlib.pyplot as plt
from notion_client import Client
import yaml

with open('.settings.yml', 'r') as f:
    config = yaml.safe_load(f)

notion = Client(auth=config['notion']['secret'])


def get_database_data(database):
    results = notion.databases.query(
        **{
            "database_id": database,
        }
    ).get("results")
    return results


def get_property_by_path(data, path):
    path_components = path.split(',')

    current_level = data
    for component in path_components:
        current_level = current_level[component.strip()]

    return current_level


def main():
    database_data = get_database_data(config['chart_data']['database']['id'])

    fig, ax = plt.subplots()

    plt.title(config['chart_data']['title'])

    for line in config['chart_data']['lines']:
        points = []

        for data in reversed(database_data):
            if line['axis'] == 'y':
                points.append(int(get_property_by_path(data, line['path'])))
            else:
                if line['type'] == 'date':
                    points.append(get_property_by_path(data, line['path']).split('T')[0])
                else:
                    points.append(get_property_by_path(data, line['path']))

        if line['axis'] == 'x':
            plt.xticks(range(len(points)), points)
        else:
            ax.plot(points, label=line['name'], color=line['color'])

    ax.legend(loc=config['chart_data']['legend'])
    plt.show()


if __name__ == '__main__':
    main()
