import React, {useEffect, useReducer} from "react";
import axios from "axios";
import UseAsync from "../components/UseAsync";
import ContestSingle from "../components/ContestSingle";



const getContests = async () => {
    const response = await axios.get(
        "api/v1/contests/contest/"
    );
    return response.data;
}

const ContestList = () => {
    const [state, fetchData] = UseAsync(getContests, []);
    const {loading, data: contests, error} = state;

    if (loading) return <div>Loading</div>
    if (error) return <div>Error</div>
    if (!contests) return null;

    return (
        <div>
            {contests.map(contest =>
                <ContestSingle
                    key={contest.id}

                    title={contest.title}
                    subtitle={contest.subtitle}
                    createdAt={contest.createdAt}
                    updatedAt={contest.updatedAt}
                    deadline={contest.deadline}
                    profileThumb={contest.profileThumb}
                    timeline={contest.timeline}
                    prize={contest.prize}
                    isForTraining={contest.isForTraining}
                    difficulty={contest.difficulty}
                    evaluationMethod={contest.evaluationMethod}
                    learningModel={contest.learningModel}

                    isScrapped={contest.isScrapped}
                    scrapNums={contest.scrapNums}
                    isFinished={contest.isFinished}
                />)
            }
        </div>
    );
};

export default ContestList;