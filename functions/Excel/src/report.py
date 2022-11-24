from .utils import *


def get_report_data(session, competitor_list, score_list, deduction_list, judge_list):
    arbitrator_ids = session['arbitratorListIds']

    # filter users by roles
    judges_a = [judge for judge in judge_list if judge['role'] == 'artistic']
    judges_e = [judge for judge in judge_list if judge['role'] == 'execution']
    judges_d = [judge for judge in judge_list if judge['role'] == 'difficulty']

    data = []

    for competitor in competitor_list:
        _id = competitor['$id']
        number = competitor['number']
        name = competitor['name']
        city = competitor['city']

        score_artistic = get_score(score_list, judges_a, _id)
        score_execution = get_score(score_list, judges_e, _id)
        score_difficulty = get_score(score_list, judges_d, _id)

        mean_artistic = get_mean_score(score_artistic)
        mean_execution = get_mean_score(score_execution)
        mean_difficult = get_mean_score(score_difficulty)

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
