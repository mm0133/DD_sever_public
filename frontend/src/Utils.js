export const getDDay = (deadline) => {
    // 2020-08-29T00:00:00+09:00
    const dDayArray = deadline.substring(0, 10).split("-").map(day => Number(day));

    const [year, month, date] = dDayArray;
    const dDay = new Date(year, month - 1, date);
    let now = new Date();
    let gap = now.getTime() - dDay.getTime();

    return Math.floor(gap / (1000 * 60 * 60 * 24)) * -1;
}

export const getDifficulty = (difficulty) => {
    switch (difficulty) {
        case "EASY":
            return {
                type: "초급",
                color: "#a7d7c5",
            }
        case "NORMAL":
            return {
                type: "중급",
                color: "#74b49b",
            }
        case "HARD":
            return {
                type: "고급",
                color: "#5c8d89",
            }
    }
}

export const getEvaluation = (evaluation) => {
    switch (evaluation) {
        case "ACCURACY":
            return "정확도 Accuracy"
        case "POPULARITY":
            return "투표 Popularity"
    }
}

export const getIsForTraining = (type) => {
    switch (type) {
        case true:
            return "연습 대회"
        case false:
            return "실전 대회"
    }
}

export const getIsFinished = (type) => {
    switch (type) {
        case true:
            return "완료"
        case false:
            return "진행중"
    }
}