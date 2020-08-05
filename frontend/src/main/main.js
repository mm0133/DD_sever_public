import React from "react";
import "./main.scss";

// fontAwesome
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrophy, faBookOpen } from "@fortawesome/free-solid-svg-icons";


function Main() {
    return (
        <div id="total-wrap">
            <header>
                <div className="logo">데이타덕 <span>Data</span>Duck</div>
                <div className="nav">
                    <a href=""><div className="nav-item">대회 목록</div></a>
                    <a href=""><div className="nav-item">강의</div></a>
                    <a href=""><div className="nav-item">토론방</div></a>
                    <a href=""><div className="nav-item">코드 공유</div></a>
                    <a href=""><div className="nav-item">사용설명서</div></a>
                    <a href=""><div className="nav-item">공지</div></a>
                    <a href=""><div className="nav-item">마이페이지</div></a>
                </div>
                <div className="logout">로그아웃</div>
            </header>

            <main-banner>
                <div className="left-side">
                    <div className="catchphrase">
                        데이타덕은<br />
                        <span>머신러닝을 즐기는 모두</span>에게<br />
                        열린 공간입니다.
                    </div>
                    <div className="button">단계별 대회 둘러보기</div>
                </div>
                <div className="logo-image"><img src="" alt=""/></div>
                <div className="contest-scrap">
                    <div className="title">스크랩한 대회</div>
                    <div className="content">스크랩한 대회가 없습니다.</div>
                    <div className="more-contest">+ 대회 둘러보기</div>
                </div>
            </main-banner>

            <contest>
                <div className="header">
                    <div className="title">
                        <div className="icon-wrap">
                            <FontAwesomeIcon icon={faTrophy} />
                        </div>
                        실전 대회 <span>대회에 참가해 실전 감각을 익혀보세요.</span>
                    </div>
                    <div className="more">실전 대회 더 둘러보기 <span>></span></div>
                </div>
            </contest>

            <contest>
                <div className="header">
                    <div className="title">
                        <div className="icon-wrap">
                            <FontAwesomeIcon icon={faBookOpen} />
                        </div>
                        연습 대회 <span className="subtitle">실전 대회가 아직 어렵다면, 연습 대회로 시작해 보세요.</span>
                    </div>
                    <div className="more">연습 대회 더 둘러보기 <span>></span></div>
                </div>
                <div className="contest-list">
                    <div className="contest">
                        <div className="contest-image"><img src="" alt=""/></div>
                        <div className="content">
                            <div className="title">얼굴 감정 인식 <span>50만</span></div>
                            <div className="subtitle">8개의 감정을 기준으로 얼굴 사진 분류하기</div>
                            <div className="timeline">
                                <div className="time">OPEN 2020.08.05.</div>
                                <div className="time">AWARD 2020.10.30.</div>
                            </div>
                        </div>
                        <div className="right-side">
                            <div className="top-side">
                                <div className="difficulty">
                                    <span className="circle"> </span> 초급
                                </div>
                                <div className="scrap"> </div>
                            </div>
                            <div className="button">참가하기</div>
                        </div>
                    </div>
                </div>
            </contest>

            <roadmap>
                <div className="title">머신러닝 로드맵</div>
                <div className="subtitle">머신러닝 기초부터 대회 참가까지, 영상으로 알아보는 머신러닝 로드맵</div>
                <div className="video-wrap">
                    <div className="arrow">&lt;</div> {/* < */}
                    <div className="video-list">
                        <div className="video">
                            <div className="video-image"><img src="" alt=""/></div>
                            <div className="right-side">
                                <div className="title">
                                    <span>1시간</span>으로 끝내는<br />
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
    )
}

export default Main;