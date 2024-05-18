// 라이브러리
// 서비스
import { getData } from "@/services/llmService";
// 컴포넌트
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import YouTube from "react-youtube";
// 아이콘
// 스타일
import "./style.css";
import { useEffect, useState } from "react";

const HomePage = () => {
    const [vid, setVid] = useState("");
    const [keywords, setKeywords] = useState([]);
    const [summary, setSummary] = useState("");
    const [quiz, setQuiz] = useState([]);
    const getVid = (url = "") => {
        let temp = url.split("v=");
        temp = temp[1].split("&");
        temp = temp[0];
        setVid(temp);
    };
    const requestGen = async () => {
        const target = document.getElementById("urlInput");
        const url = target.value;
        if (url !== "") {
            getVid(url);
            const response = await getData(vid);
            if (!response.err) {
                setKeywords(response.keyword);
                setSummary(response.summary);
                console.log(response.quiz);
                setQuiz(response.quiz);
            }
        }
    };
    return (
        <div id="homePage" className="page">
            <div className="searchContainer">
                <Input
                    id="urlInput"
                    type="text"
                    placeholder="Input Youtube Video Url"
                />
                <Button onClick={requestGen}>Generate</Button>
            </div>
            <div className="videoContainer">
                {vid === "" ? (
                    <div className="noVideo">No Video Result!!</div>
                ) : (
                    <YouTube
                        videoId={vid}
                        id="youtubePlayer"
                        className={`video_id_${vid}`}
                        opts={{
                            playerVars: {
                                autoplay: 1,
                                rel: 0,
                                modestbranding: 1,
                            },
                        }}
                    />
                )}
            </div>
            <div className="summaryContainer">
                <h1 className="containerTitle">Summary Video</h1>
                <div className="summaryWrap">
                    <p className="summaryItem">{summary}</p>
                </div>
            </div>
            <div className="quizContainer">
                <h1 className="containerTitle">Quiz</h1>
                <div className="quizWrap">
                    {quiz.map((question, idx) => (
                        // <QuestionItem data={question} idx={idx} />
                        <p>123123</p>
                    ))}
                </div>
            </div>
        </div>
    );
};

const QuestionItem = ({ data, idx }) => {
    console.log(data);
    return (
        <div className="questionWrap">
            <p className="question" key={`questionItem${idx + 1}`}>
                Q{data.question}
            </p>
            <div className="optionWrap">
                {data.options.map((option, idx) => (
                    <button className="optionItem" key={`optionItem${idx + 1}`}>
                        {option}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default HomePage;
