from conftest import CANDIDATE_COUNT


class TestCreateCandidatesBulk:
    # End-to-end test: reuse logged-in fixture, then create CANDIDATE_COUNT candidates.
    def test_create_many_candidates_via_add_candidate_ui(self, candidate_page):
        for _ in range(CANDIDATE_COUNT):
            candidate_page.create_candidate()
