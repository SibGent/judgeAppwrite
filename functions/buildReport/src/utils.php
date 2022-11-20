<?php

function getUserNames($juryNameList, $userId) {
    foreach ($juryNameList as $item) {
        if ($item['$id'] == $userId) {
            return $item['name'];
        }
    }

    return $userId;
}

function searchScore($array, $competitorId, $judgeId) {
    $value = 0.0;

    foreach ($array as $key) {
        if ($key['judgeId'] == $judgeId && $key['competitorId'] == $competitorId) {
            $value = (float) $key['value'];
            break;
        }
    }

    return $value;
}

function searchDeduction($array, $competitorId, $arbitratorId) {
    $value = 0.0;

    foreach ($array as $key) {
        if ($key['arbitratorId'] == $arbitratorId && $key['competitorId'] == $competitorId) {
            $value = (float) $key['value'];
            break;
        }
    }

    return $value;
}

function sumTotal($score, $deduction) {
    $total = 0.0;

    foreach ($score as $key => $value) {
        $total += $value;
    }

    foreach ($deduction as $key => $value) {
        $total -= $value;
    }

    return $total;
}