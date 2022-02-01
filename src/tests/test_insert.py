# from main import insert_regression_summary
# from models.types import RegressionSummaryPayload
# from datetime import datetime, timezone
# from typing import List
# import unittest
# import os, asyncio

# model_summary_template = {
#     "created_time": "1900-01-01T01:01:01.000000+00:00",
#     "name": "testSummary",
#     "desc": "string",
#     "target": "string",
#     "prediction": "string",
#     "var_weights": "string",
#     "link_function": "string",
#     "error_dist": "string",
#     "explained_variance": 0,
#     "feature_summary": [
#         {
#             "name": "string",
#             "data": {
#                 "bin_edge_right": [0],
#                 "sum_target": [0],
#                 "sum_prediction": [0],
#                 "sum_weight": [0],
#                 "wtd_avg_prediction": [0],
#                 "wtd_avg_target": [0],
#             },
#         }
#     ],
# }


# class TestInsertRegressionSummary(unittest.IsolatedAsyncioTestCase):
#     # violates snake-case naming convention
#     def setUp(self):
#         # sample data structure
#         self.test_data_template: RegressionSummaryPayload = model_summary_template

#     # violates snake-case naming convention
#     def tearDown(self):
#         del self.test_data_template

#     async def test_insert_different_date_types(self):
#         # set up test cases
#         model_summary = self.test_data_template.copy()
#         test_cases = [
#             "1900-01-01T01:01:01.000000+00:00",  # string
#             datetime.utcnow(),  # datetime, not timezone aware
#             datetime.now(timezone.utc),  # datetime, timezone aware
#         ]

#         # try each test case
#         test_results: List[str] = []
#         for test_case in test_cases:
#             model_summary.update({"created_time": test_case})
#             api_response: str = await insert_regression_summary(model_summary)
#             test_results.append(api_response)

#         # check that we have a valid response with our test data
#         for test_result in test_results:
#             self.assertEqual(test_result, "okk")


# if __name__ == "__main__":
#     unittest.main(verbosity=2)
