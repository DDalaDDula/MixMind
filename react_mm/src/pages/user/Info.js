import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function Info() {
    const navigate = useNavigate();
    const location = useLocation();
    const [email, setEmail] = useState();
    const [nickname, setNickname] = useState();
    const [age, setAge] = useState();

    useEffect(() => {
        setEmail(location.state.info.email)
        setNickname(location.state.info.nickname)
        setAge(location.state.info.age)
    }, [])

    const editInfo = async() => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/user/edit/${location.state.info.id}/`, {
                method: 'put',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    nickname,
                    age,
                }),
            });

            if (response.ok) {
                alert('수정이 완료되었습니다.');
            } else {
                const data = await response.json();
                alert(data.message);
            }

        } catch (error) {
            console.error('수정 중 오류 발생:', error);
        }

        navigate('/')
    }

    return(
        <div>
            <input
                type="email"
                placeholder="이메일"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="text"
                placeholder="닉네임"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
            />
            <input
                type="number"
                placeholder="나이"
                value={age}
                onChange={(e) => setAge(e.target.value)}
            />
            <button onClick={editInfo}>수정</button>
        </div>
    )
}