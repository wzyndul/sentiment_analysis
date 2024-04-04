import base64
import io

from matplotlib import pyplot as plt
import matplotlib.dates as mdates


def sentiment_over_time(data):
    plt.figure(dpi=100)
    plt.plot(data.keys(), data.values())

    # TODO based on the time range, set the x-axis format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.title('Sentiment over time')
    plt.xlabel('Timestamp')
    plt.ylabel('Average sentiment')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return plot_data
