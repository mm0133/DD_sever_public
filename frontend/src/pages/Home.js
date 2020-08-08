import React from "react";
import "./Home.scss";
import logo from "../image/logo.png"

// fontAwesome
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTrophy, faBookOpen, faStar, faUser, faCalendar, faAward} from "@fortawesome/free-solid-svg-icons";
import {faStar as faStarLine} from "@fortawesome/free-regular-svg-icons";
import {NavLink} from "react-router-dom";
import ContestSingle from "../components/ContestSingle";


const Home = () => {
    return (
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
                    <ContestSingle />
                    <ContestSingle />
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
                        <div className="subtitle">실전 대회가 아직 어렵다면, 연습 대회로 시작해 보세요.</div>
                    </div>
                    <div className="more">연습 대회 더 둘러보기<span>></span></div>
                </div>
                <div className="contest-list">
                    <div className="contest">
                        <div className="content-wrap">
                            <div className="contest-image"><img src="" alt=""/></div>
                            <div className="content">
                                <div>
                                    <div className="title">얼굴 감정 인식<span>연습</span></div>
                                    <div className="subtitle">
                                        8개의 감정을 기준으로 얼굴 사진 분류하기
                                        <span className="bar">ㅣ</span>
                                        <span className="classification">분류</span>
                                    </div>
                                </div>
                                <div className="summary-wrap">
                                    <div className="summary">
                                        <div className="icon-wrap">
                                            <FontAwesomeIcon icon={faUser} className="icon"/>
                                        </div>
                                        <div>20팀</div>
                                    </div>
                                    <div className="summary">
                                        <div className="icon-wrap">
                                            <FontAwesomeIcon icon={faCalendar} className="icon"/>
                                        </div>
                                        <div>D-120</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="participate">
                            <div className="top-side">
                                <div className="difficulty">
                                    <div className="circle"></div>
                                    초급
                                </div>
                                <FontAwesomeIcon icon={faStarLine} className="scrap"/>
                            </div>
                            <div className="button">
                                <div className="overlay">
                                    참가하기
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="contest">
                        <div className="content-wrap">
                            <div className="contest-image"><img src="" alt=""/></div>
                            <div className="content">
                                <div>
                                    <div className="title">LOL 승률 예측<span>연습</span></div>
                                    <div className="subtitle">LOL 데이터로 팀 승률 예측하기
                                        <span className="bar">ㅣ</span>
                                        <span className="classification">예측</span>
                                    </div>
                                </div>
                                <div className="summary-wrap">
                                    <div className="summary">
                                        <div className="icon-wrap">
                                            <FontAwesomeIcon icon={faUser} className="icon"/>
                                        </div>
                                        <div>20팀</div>
                                    </div>
                                    <div className="summary">
                                        <div className="icon-wrap">
                                            <FontAwesomeIcon icon={faCalendar} className="icon"/>
                                        </div>
                                        <div>D-120</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="participate">
                            <div className="top-side">
                                <div className="difficulty">
                                    <div className="circle"></div>
                                    초급
                                </div>
                                <FontAwesomeIcon icon={faStarLine} className="scrap"/>
                            </div>
                            <div className="button">
                                <div className="overlay">
                                    참가하기
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </contest>

            <roadmap>
                <div className="title">머신러닝 로드맵</div>
                <div className="subtitle">머신러닝 기초부터 대회 참가까지, 영상으로 알아보는 머신러닝 로드맵</div>
                <div className="video-wrap">
                    <div className="arrow">&lt;</div>
                    {/* < */}
                    <div className="video-list">
                        <div className="video">
                            <div className="video-image"><img src="" alt=""/></div>
                            <div className="right-side">
                                <div className="title">
                                    <span>1시간</span>으로 끝내는<br/>
                                    머신러닝 <span>기초</span>
                                </div>
                                <div className="video-button">무료 강의 보러가기 ></div>
                            </div>
                        </div>
                        <div className="video">
                            <div className="video-image"><img src="" alt=""/></div>
                            <div className="right-side">
                                <div className="title">
                                    <div className="classification"><span>대회</span> 대회 톺아보기</div>
                                    감정 인식 대회 <span>EDA</span>
                                </div>
                                <div className="video-button">무료 강의 보러가기 ></div>
                            </div>
                        </div>
                        <div className="video">
                            <div className="video-image"><img src="" alt=""/></div>
                            <div className="right-side">
                                <div className="title">
                                    <div className="classification"><span>대회</span> 대회 톺아보기</div>
                                    감정 인식 대회 <span>전처리</span>
                                </div>
                                <div className="video-button">무료 강의 보러가기 ></div>
                            </div>
                        </div>
                    </div>
                    <div className="arrow">></div>
                </div>
            </roadmap>

            <mannual>
                <div className="subtitle">당신을 위한 <span>완벽한</span> 데이타덕 가이드</div>
                <div className="title">데이타덕 <span>사용설명서</span></div>
            </mannual>

            <footer>
            </footer>
        </div>
    );
};

export default Home;