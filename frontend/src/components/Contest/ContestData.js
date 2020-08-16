import React from "react";
import "./ContestData.scss";

const ContestData = (props) => {
    console.log("contestData");

    return (
        <div className="total-wrap data">
            <div className="data-text">
                <div className="title">데이터 설명</div>
                <div className="content">{props.dataExplanation}</div>
            </div>
            <div className="data-download">
                <div className="title">데이터 다운로드<span>(24.18 GB)</span></div>
                <div className="content-wrap">
                    <div className="content">
                        <div className="subtitle">파일 목록</div>
                        <div className="text"></div>
                    </div>
                    <div className="content">
                        <div className="subtitle">파일 상세</div>
                        <div className="text">
                            <div><span>파일명</span>파일 이름 여기</div>
                            <div><span>크기</span>4.6 GB</div>
                            <div><span>데이터 개수</span>1230개</div>
                        </div>
                    </div>
                    <div className="content">
                        <div className="subtitle">컬럼</div>
                        <div className="text">
                            <div><span>컬럼 이름1</span>컬럼 이름 설명1</div>
                            <div><span>컬럼 이름2</span>컬럼 이름 설명2</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ContestData;