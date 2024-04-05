import base64
import io

from matplotlib import pyplot as plt
import matplotlib.dates as mdates


def sentiment_plot(data):
    plt.figure(dpi=100)
    plt.plot(data.keys(), data.values())

    keys = list(data.keys())
    time_range = keys[-1] - keys[0]  # time_range return days and seconds between the first and last date
    # for example if time period is 34 hours, it will return 1 day and 36000 seconds (10 hours)

    if 1 < time_range.days < 31:
        interval = 1
        if time_range.days > 20:
            interval = 2
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        plt.xlabel('months and days')

    elif 31 <= time_range.days < 365:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xlabel('years and months')

    elif time_range.days >= 365:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.xlabel('years')
    else:
        interval = 1
        if time_range.days >= 1:
            interval = 2
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%H'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=interval))
        plt.xlabel('Days and hours UTC')

    plt.xticks(rotation=45)
    plt.title('Sentiment over time')

    plt.ylabel('Average sentiment')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()



    return plot_data
