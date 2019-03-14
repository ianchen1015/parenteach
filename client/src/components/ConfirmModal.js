import React, { Component } from 'react';
import { Modal, Message, Form, TextArea, Button, Feed, Header } from 'semantic-ui-react';

class ConFirmModal extends Component {
    state = { text: '' };
    
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
                                placeholder='告訴家長的話'
                                value={this.state.text}
                                onChange={ e => this.setState({text: e.target.value}) }
                            />
                        </Form>
                    </Modal.Description>
                </Modal.Content>
                
                <Modal.Actions>
                    <Button onClick={ () => {this.props.onFinishModal(false)} } negative>取消</Button>
                    <Button onClick={ () => {this.props.onFinishModal(true, this.state.text)} } positive>發送</Button>
                </Modal.Actions>
            </Modal>
        );
    }
}

export default ConFirmModal;