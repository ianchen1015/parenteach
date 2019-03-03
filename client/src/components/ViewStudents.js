import React from 'react';
import { Container, Grid, Button, Checkbox, Modal } from 'semantic-ui-react';

import './ViewStudents.css';

class ViewStudents extends React.Component {
    state = {
        status: 'viewing',
        students: [ {name: '陸佩宜', number: 1}, {name: '孟雅恩', number: 2}, {name: '韋晉唯', number: 3}, {name: '賀恆慈', number: 4}, 
            {name: '程佳玲', number: 5}, {name: '吳詠絮', number: 6}, {name: '麥哲瑋', number: 7}, {name: '武維宇', number: 8}, 
            {name: '馬惠婷', number: 9}, {name: '符正棻', number: 10}, {name: '郝珮瑄', number: 11}, {name: '朱﻿明達', number: 12}, 
            {name: '倪瓊之', number: 13}, {name: '田育秋', number: 14}, {name: '邵禹凡', number: 15}, {name: '趙振翔', number: 16} ],
    }
    
    renderStudentsStatus() {
        return this.state.students.map(student => {
            return (
                <Grid.Column width={4} key={student.number}>
                    <div className="user-icon-wrap">
                        { this.state.status==='editting'? <Checkbox className="absent-checkbox" />: null}
                        <div className="user-number">{student.number}</div>
                        <div className="user-icon-head"></div>
                        <div className="user-icon-body"></div>
                        <div className="user-name">{student.name}</div>
                    </div>
                </Grid.Column>);
        });
    }
    
    onChangeStatus = () => {
        switch (this.state.status) {
            case 'viewing':
                this.setState({status: 'editting'});
                break;
            case 'editting':
                this.setState({status: 'confirmingSaving'});
                break;
            case 'confirmingSaving':
                break;
            default:
                break;
        }
    }
    
    onSavingConfirmed = () => {
        this.setState({status: 'viewing'});
    }
    
    render() {
        const editButtonWord = this.state.status==='editting'? "儲存出缺席" : "編輯出缺席";
        return (
            <Container className="viewstudents">
                <Grid>
                    <Grid.Column id="upper-buttons" width={16}>
                        <Button compact floated="left" size="tiny">2019 年 1 月 01 日</Button>
                        <Button compact floated="right" size="tiny" basic color="blue"
                            onClick={this.onChangeStatus}
                        >
                            {editButtonWord}
                        </Button>
                    </Grid.Column>
                    {this.renderStudentsStatus()}
                </Grid>
                <Modal 
                    open={this.state.status==='confirmingSaving'}
                    closeOnDimmerClick={false}
                >
                    <Modal.Header>header</Modal.Header>
                    <Modal.Content>content</Modal.Content>
                    <Modal.Actions>
                        <Button onClick={this.onSavingConfirmed} positive>發送</Button>
                    </Modal.Actions>
                </Modal>
            </Container>
        );
    }
}

export default ViewStudents;