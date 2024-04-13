from datetime import datetime

from sentiment_app.predict import predict_sentiment


def video_sentiment_preprocess(comments):
    sorted_comments = sorted(comments.items(),
                             key=lambda item: datetime.strptime(item[1]['comment_time'], "%Y-%m-%dT%H:%M:%S%z"))
    sentiments_over_time = {}
    positive = 0
    all = 0
    for comment_id, comment_data in sorted_comments:
        all += 1
        comment = comment_data['comment']
        comment_time = comment_data['comment_time']
        result = predict_sentiment(comment)
        timestamp = datetime.strptime(comment_time, "%Y-%m-%dT%H:%M:%S%z")
        timestamp = timestamp.replace(minute=0, second=0)
        if result == 1:
            positive += 1
        sentiment = positive / all
        sentiments_over_time[timestamp] = sentiment

    negative = len(comments) - positive
    num_comments = len(comments)
    if len(comments) == 0:
        rating = 0
    else:
        rating = round(positive / len(comments) * 100, 2)
    stats = {
        'num_comments': num_comments,
        'positive': positive,
        'negative': negative,
        'rating': rating
    }
    return sentiments_over_time, stats
