from agents.marketing_analytics.marketing_analyst_agent import marketingAnalyticsAgent

DATA_PATH = (
    "data/marketing/shopee_ads/overall_data/"
    "Shopee-Ads-Overall-Data-01_09_2026-21_09_2026.csv"
)

def test_get_observations_and_queries():
    marketing_analytics_agent = marketingAnalyticsAgent()

    report = marketing_analytics_agent.get_observations_and_queries(DATA_PATH)

    assert isinstance(report, dict)
    assert isinstance(report.get("relevant_observations"), list)
    assert isinstance(report.get("relevant_query"), str)
    assert report["relevant_observations"]
    assert report["relevant_query"].strip()
    print ("Test passed!")


def test_analyse_marketing_performance_pipeline():
    marketing_analytics_agent = marketingAnalyticsAgent()
    retriever = "term"

    solution = marketing_analytics_agent.analyse_marketing_performance_pipeline(
        marketing_data_path=DATA_PATH,
        retriever=retriever,
    )

    assert solution
    print(f"Pipeline test passed!")

if __name__ == "__main__":
    #test_get_observations_and_queries()
    test_analyse_marketing_performance_pipeline()
