import React, {useEffect, useState} from "react";
import ContestSingle from "../Contest/ContestSingle";
import {NavLink} from "react-router-dom";
import {getContestList} from "../../Api";

import "./Home.scss";
import logo from "../../image/logo.png";

// fontAwesome
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTrophy, faBookOpen} from "@fortawesome/free-solid-svg-icons";


const Home = () => {
    const [contests, setContests] = useState([]);

    useEffect(() => {
        const init = async () => {
            const data = await getContestList();

            setContests(data);
        }
        init();
    }, [])

    console.log(contests);

    const contestForTraining = contests ? contests.filter(contest => contest.isForTraining) : null;
    const contestNotForTraining = contests ? contests.filter(contest => !contest.isForTraining) : null;

    return (
        <div>
            {!contests ? <div>{null}</div> :
                <div className="total-wrap">
                    <main-banner>
                        <div style={{zIndex: 1}}>
                            {/* logo 위에 catchphrase + button */}
                            <div className="catchphrase">
                                데이타덕은<br/>
                                <span>머신러닝을 원하는 모두</span>에게<br/>
                                열린 공간입니다.
                            </div>
                            <NavLink to="/contest" className="link">
                                <div className="button">
                                    <div className="overlay">단계별 대회 둘러보기</div>
                                </div>
                            </NavLink>
                        </div>
                        <div className="logo-image"><img src={logo} alt=""/></div>
                        <div className="contest-scrap">
                            <div>
                                <div className="title">스크랩한 대회</div>
                                <div className="content">스크랩한 대회가 없습니다.</div>
                            </div>
                            <NavLink to="/contest" className="link more-contest">+ 대회 둘러보기</NavLink>
                        </div>
                    </main-banner>

                    {/* 실전 대회 */}
                    <contest>
                        <div className="header">
                            <div className="title">
                                <div className="icon-wrap">
                                    <FontAwesomeIcon icon={faTrophy} className="icon"/>
                                </div>
                                <div>실전 대회</div>
                                <div className="subtitle">대회에 참가해 실전 감각을 익혀보세요.</div>
                            </div>
                            <div className="more">실전 대회 더 둘러보기<span>></span></div>
                        </div>
                        <div className="contest-list">
                            {contestNotForTraining.slice(0, 2).map(contest =>
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
                    </contest>

                    {/* 연습 대회 */}
                    <contest>
                        <div className="header">
                            <div className="title">
                                <div className="icon-wrap">
                                    <FontAwesomeIcon icon={faBookOpen} className="icon"/>
                                </div>
                                <div>연습 대회</div>
                                <div className="subtitle">머신러닝 학습, 연습 대회로 시작해 보세요.</div>
                            </div>
                            <div className="more">연습 대회 더 둘러보기<span>></span></div>
                        </div>
                        <div className="contest-list">
                            {contestForTraining.slice(0, 2).map(contest =>
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
                    </contest>

                    <div className="roadmap">
                        <div className="title">머신러닝 로드맵</div>
                        <div className="subtitle">
                            <div className="text">머신러닝 기초부터 대회 참가까지, 영상으로 알아보는 머신러닝 로드맵</div>
                            <div className="more">로드맵 따라가기<span>></span></div>
                        </div>
                        <div className="video-list">
                            <div className="video" style={{backgroundImage: "url()"}}>
                                <div className="title">
                                    <span>1시간</span>으로 끝내는<br/>
                                    머신러닝 <span>기초</span>
                                </div>
                                <div className="video-button">
                                    <div className="overlay">
                                        무료 강의 보러가기 <span>></span>
                                    </div>
                                </div>
                            </div>
                            <div className="video" style={{backgroundImage: "url()"}}>
                                <div className="title">
                                    <div className="classification">
                                        <div className="circle">대회</div>
                                        대회 톺아보기
                                    </div>
                                    감정 인식 대회 <span>EDA</span>
                                </div>
                                <div className="video-button">
                                    <div className="overlay">
                                        무료 강의 보러가기 <span>></span>
                                    </div>
                                </div>
                            </div>
                            <div className="video" style={{backgroundImage: "url()"}}>
                                <div className="title">
                                    <div className="classification">
                                        <div className="circle">대회</div>
                                        대회 톺아보기
                                    </div>
                                    감정 인식 대회 <span>전처리</span>
                                </div>
                                <div className="video-button">
                                    <div className="overlay">
                                        무료 강의 보러가기 <span>></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="manual">
                        <div className="subtitle">당신을 위한<span>완벽한</span>데이타덕 가이드</div>
                        <div className="title">데이타덕 <span>사용설명서</span></div>
                    </div>
                </div>
            }
        </div>
    );
};

export default Home;