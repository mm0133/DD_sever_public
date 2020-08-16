import React, {useEffect, useState} from "react";
import {getContestList} from "../../Api";
import ContestSingle from "./ContestSingle";
import "./ContestList.scss"


const ContestList = () => {
    const [filter, setFilter] = useState([]);
    const [contests, setContests] = useState([]);
    const [keyword, setKeyword] = useState("");

    useEffect(() => {
        const init = async () => {
            const data = await getContestList();

            setContests(data);
            setFilter(data);
        }
        init();
    }, [])

    const getContestAll = () => {
        setFilter(contests);
    }

    const getContestForTraining = async () => {
        setFilter(contests.filter(contest => contest.isForTraining));
    }

    const getContestNotForTraining = async () => {
        setFilter(contests.filter(contest => !contest.isForTraining));
    }

    const getKeyword = (e) => {
        setKeyword(e.target.value);
        console.log(keyword);
        setFilter(filter.filter(search => search.title.indexOf(keyword) > -1));
        console.log(filter);
    }

    const length = contests ? filter.length : null;


    return (
        <div>
            {!filter ? <div>{null}</div> :
                <div className="total-wrap">
                    <div className="list-main-banner">
                        <div className="title">대회 Contest</div>
                        <div className="subtitle">머신러닝을 원하는 모두를 위한 대회입니다.</div>
                    </div>

                    <div className="list-nav">
                        <div className="button-list">
                            <div className="buttons">
                                <button className="button" onClick={getContestAll}>전체</button>
                                <button className="button" onClick={getContestForTraining}>실전 대회</button>
                                <button className="button" onClick={getContestNotForTraining}>연습 대회</button>
                            </div>
                            <div>총 {length}개의 대회</div>
                        </div>

                        <div className="tag-list">
                            <div className="tags">
                                <button className="tag">#초급</button>
                                <button className="tag">#중급</button>
                                <button className="tag">#고급</button>
                            </div>
                            <input
                                type="text"
                                placeholder="대회 검색"
                                onChange={getKeyword}
                                value={keyword}
                            />
                        </div>
                    </div>

                    <div className="list-contest">
                        <div>
                            {filter.map(contest =>
                                <ContestSingle
                                    key={contest.id}

                                    id={contest.id}
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
                    </div>
                </div>
            }
        </div>
    );
}

export default ContestList;