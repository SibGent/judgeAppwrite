def get_max_col(array):
    count = 0

    for v in array.values():
        if type(v) is dict:
            count += len(v)
            continue

        count += 1

    return count


def get_score(score_list, judges, competitor_id):
    result = {}

    for judge in judges:
        judge_id = judge['userId']
        judge_number = judge['number']
        key = f'C{judge_number}'

        result[key] = 0.0

        for score in score_list:
            if score['userId'] == judge_id and score['competitorId'] == competitor_id:
                result[key] = score['value']
                break

    return result


def get_deduction(deduction_list, judges, arbitrator_ids, competitor_id):
    result = {}

    for judge in judges:
        judge_id = judge['userId']
        judge_number = judge['number']
        key = f'C{judge_number}'

        result[key] = 0.0

        for score in deduction_list:
            if score['userId'] == judge_id and score['competitorId'] == competitor_id:
                result[key] = score['value']
                break

    arbitrator_index = 0

    for arbitrator_id in arbitrator_ids:
        arbitrator_index += 1
        key = f'A{arbitrator_index}'

        result[key] = 0.0

        for score in deduction_list:
            if score['userId'] == arbitrator_id and score['competitorId'] == competitor_id:
                result[key] = score['value']
                break

    return result


def get_mean_score(score_list):
    score_sum = sum(score_list.values())

    if score_sum == 0:
        return 0

    score_count = len(score_list)
    return float(score_sum) / score_count


def get_sum_deduction(dedution_list):
    deduction_sum = sum(dedution_list.values())

    if deduction_sum == 0:
        return 0

    return deduction_sum


def get_total(mean_artistic, mean_execution, mean_difficult, deduction):
    return mean_artistic + mean_execution + mean_difficult - deduction
