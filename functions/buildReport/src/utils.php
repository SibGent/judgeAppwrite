<?php
function getJudgeIds($array, $key, $keyValue): array
{
    $filter = array_filter($array, function($value) use ($key, $keyValue) {
        return $value[$key] == $keyValue;
    });

    return array_column($filter, 'userId');
}

function getScore($score, $judgeIds, $competitorId): array
{
    $res = [];

    foreach ($judgeIds as $judgeId) {
        $filter = array_filter($score, function($value) use ($judgeId, $competitorId) {
            return $value['judgeId'] == $judgeId && $value['competitorId'] == $competitorId;
        });
        $value = array_column($filter, 'value')[0];

        $res[$judgeId] = $value;
    }

return $res;
}

function getDeduction($deduction, $judgeIds, $competitorId): array
{
    $res = [];

    foreach ($judgeIds as $judgeId) {
        $filter = array_filter($deduction, function($value) use ($judgeId, $competitorId) {
            return $value['arbitratorId'] == $judgeId && $value['competitorId'] == $competitorId;
        });
        $value = array_column($filter, 'value')[0];

        $res[$judgeId] = $value;
    }

return $res;
}

function getMeanScore($scores): float
{
    $values = array_values($scores);
    return array_sum($values) / count($values);
}

function getTotal($meanArtistic, $meanDifficulty, $meanExecution, $deduction): float
{
    return $meanArtistic + $meanDifficulty + $meanExecution + array_sum(array_values($deduction));
}

function sortByTotal($out): array
{
    uasort($out, function($a, $b) {
        if ($a['total'] == $b['total']) {
            return 0;
        }

        return $a['total'] < $b['total'] ? 1 : -1;
    });

    return array_values($out);
}