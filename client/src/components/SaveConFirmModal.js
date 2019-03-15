import React, { Component } from 'react';
import { Modal, Button, Header, Container } from 'semantic-ui-react';
import './SaveConFirmModal.css';

class SaveConFirmModal extends Component {
    state = { text: '⚠️ 尚未到校\n今日 (1/03) 您的孩子尚未抵達教室，請問他是否需要請假呢？' };
    
    render() {
        return(
            <Modal 
                open
                onClose={() => { this.props.onFinishModal(false) }}
                closeIcon
            >
                <Modal.Header>已儲存更新</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        <Container className='container'>
                            <Header>傳送給已到校學生的家長</Header>
                            <Button primary onClick={ () => { this.props.onFinishModal(false); } }>平安到校</Button>
                        </Container>
                        <Container className='container'>
                            <Header>傳送給未到校學生的家長</Header>
                            <Button primary onClick={ () => {
                                this.props.sendAbsentMessage();
                            } }>詢問缺席原因</Button>
                        </Container>
                    </Modal.Description>
                </Modal.Content>
                
                <Modal.Actions>
                    <Button onClick={ () => {this.props.onFinishModal(false)} } >關閉</Button>
                </Modal.Actions>
            </Modal>
        );
    }
}

export default SaveConFirmModal;