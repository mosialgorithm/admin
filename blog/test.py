print('user most news', 'user_most_news')
    # ==================================
    sum_seen = 0
    for news in news_most_seen:
        sum_seen += news.views
    print('sum of all news is : ',sum_seen)
    # ==================================
    for news in 'user_most_news':
        print(news.user_id)
        print(news.title)
        print(news.views)
        print(news.writer(news.user_id))
        print('='*30)
    # -------------------------------------------------------
    # all_writers = News.query.group_by(News.user_id).all()
    # sum_views_by_user = News.query.filter_by(News.user_id in all_writers[News.user_id]).all()
    writers = []
    for wr in 'all_writers':
        writers.append(wr.user_id)
    print('0'*50)
    print('all writers are :', writers)
    print('0'*50)
    # -------------------------------------------------------
    print('@'*50)
    # print(sum_views_by_user)
    print('@'*50)