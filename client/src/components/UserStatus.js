import styled from 'styled-components';

const UserIconWrap = styled.div`
    width: 60px;
    height: 80px;
`;

const UserIconHead = styled.div`
    border-radius: 50%;
    border: 3px white solid;
    background-color: #E05400;
    width: 30px;
    height: 30px;
    margin: auto;
    position: absolute;
    left: 0;
    right: 0;
    z-index: 2;
    top: 34px;
`;

const UserIconBody = styled.div`
    width: 50px;
    height: 40px;
    background-color: #E05400;
    border-radius: 30px 30px 6px 6px;
    margin: auto;
    left: 0;
    right: 0;
    top: 51px;
    position: absolute;
`;

const UserNumber = styled.div`
    position: absolute;
    width: 100%;
    margin: auto;
    left: 0;
    top: 41px;
    color: white;
    z-index: 3;
    text-align: center;
`;

const UserName = styled.div`
    position: absolute;
    z-index: 3;
    margin: auto;
    left: 0;
    right: 0;
    width: 100%;
    text-align: center;
    top: 68px;
    color: white;
`;

export { UserIconHead, UserName, UserNumber, UserIconBody, UserIconWrap };