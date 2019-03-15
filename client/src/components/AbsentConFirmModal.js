import React, { Component } from 'react';
import { Modal, Message, Form, TextArea, Button, Feed, Header } from 'semantic-ui-react';
import $ from 'jquery'; 

class AbsentConFirmModal extends Component {
    state = { text: '⚠️ 尚未到校\n今日 (1/03) 您的孩子尚未抵達教室，請問他是否需要請假呢？' };
    
    render() {
        const studentsFeed = this.props.selectedStudents.map(studentName => {
            return (
                <Feed.Event
                    icon='user circle'
                    summary={studentName}
                    key={studentName}
                />
            );
        })

        return(
            <Modal 
                open
                onClose={() => { this.props.onFinishModal(false) }}
                closeIcon
            >
                <Modal.Header>「缺席詢問」發送確認</Modal.Header>
                <Modal.Content>
                    <Message info content='訊息將自動傳送，是否發送？' />
                    <Modal.Description>
                        <Header>發送對象</Header>
                        <Feed>{studentsFeed}</Feed>
                        <Header>訊息內容</Header>
                        <Form>
                            <TextArea 
                                value={this.state.text}
                                onChange={ e => this.setState({text: e.target.value}) }
                            />
                        </Form>
                    </Modal.Description>
                </Modal.Content>
                
                <Modal.Actions>
                    <Button onClick={ () => {this.props.onFinishModal(false)} } negative>取消</Button>
                    <Button onClick={ () => {
                        this.props.onFinishModal(true, this.state.text);
                        $.get('https://parenteach.herokuapp.com/absent');
                    } } positive>發送</Button>
                </Modal.Actions>
            </Modal>
        );
    }
}

export default AbsentConFirmModal;