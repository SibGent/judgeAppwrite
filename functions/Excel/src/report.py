import statistics
from .utils import *


def get_report_data(session, competitor_list, score_list, deduction_list):
    arbitrator_ids = session['arbitratorListIds']
    judges_a = session['judgeArtisticListIds']
    judges_e = session['judgeExecutionListIds']
    judges_d = session['judgeDifficultyListIds']

    data = []

    for competitor in competitor_list:
        _id = competitor['$id']
        number = competitor['number']
        name = competitor['name']
        city = competitor['city']

        score_artistic = get_score(score_list, judges_a, _id, 'А')
        score_execution = get_score(score_list, judges_e, _id, 'И')
        score_difficulty = get_score(score_list, judges_d, _id, 'С')

        mean_artistic = statistics.median(score_artistic.values())
        mean_execution = statistics.median(score_execution.values())
        mean_difficult = statistics.median(score_difficulty.values())

        deduction = get_deduction(deduction_list, judges_d, arbitrator_ids, _id)
        sum_deduction = get_sum_deduction(deduction)

        total = get_total(mean_artistic, mean_execution, mean_difficult, sum_deduction)

        data.append({
            'number': number,
            'name': name,
            'city': city,
            'scoreArtistic': score_artistic,
            'meanArtistic': mean_artistic,
            'scoreExecution': score_execution,
            'meanExecution': mean_execution,
            'scoreDifficulty': score_difficulty,
            'meanDifficult': mean_difficult,
            'deduction': deduction,
            'sumDeduction': sum_deduction,
            'total': total,
        })

    # sort by total
    sorted_data = sorted(data, key=lambda d: d['total'], reverse=True)

    # added place
    place = 1
    for x in sorted_data:
        x['place'] = place
        place += 1

    return sorted_data
