import React, {useEffect, useState} from "react";
import {NavLink, Route} from "react-router-dom";
import {getContests} from "../Api";
import ContestSingle from "../components/ContestSingle";
import axios from "axios";
import useAsync from "../UseAsync";


const ContestList = () => {
    const [state, refetch] = useAsync(getContests, []);
    const {data: contests} = state;

    let filter = contests ? contests : null;
    console.log(filter);

    const getContestForTraining = () => {
        filter = contests ? contests.filter(contest => contest.isForTraining) : null;
    }
    const getContestNotForTraining = () => {
        filter = contests ? contests.filter(contest => !contest.isForTraining) : null;
        console.log(filter);
    }

    return (
        <div>
            {!contests ? <div>{null}</div> :
                <div className="total-wrap">
                    <main-banner>
                        <div className="title">대회 Contest</div>
                        <div className="subtitle">머신러닝을 원하는 모두를 위한 대회입니다.</div>
                    </main-banner>

                    <nav>
                        <div className="button-list">
                            <div className="button">전체</div>
                            <button className="button" onClick={getContestNotForTraining}>실전 대회</button>
                            <div className="button">연습 대회</div>
                        </div>

                        <div className="tag-list">
                            <div className="tag">초급</div>
                            <div className="tag">중급</div>
                            <div className="tag">고급</div>
                        </div>
                    </nav>

                    <contest>
                        <div>
                            {filter.map(contest =>
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
                    </contest>
                </div>
            }
        </div>
    );
};

export default ContestList;