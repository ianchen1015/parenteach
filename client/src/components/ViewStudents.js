import React from 'react';
import { Container, Grid, Button, Checkbox} from 'semantic-ui-react';
import _ from 'lodash';

import { UserIconHead, UserName, UserNumber, UserIconBody, UserIconWrap } from './UserStatus';
import SaveConFirmModal from './SaveConFirmModal';
import AbsentConFirmModal from './AbsentConFirmModal';
import defaultStudents from '../defaultStudents';
import './ViewStudents.css';

const status = {
    viewing: 0,
    editing: 1,
    saveConfirmingSaving: 2,
    absentConfirmingSaving: 3,
}

class ViewStudents extends React.Component {
    state = {
        status: status.viewing,
        students: defaultStudents,
        selectedStudents: [],
    }
    
    onStudentAbsentSelected = number => {
        const student = _.find(this.state.students, i => i.number===number );
        if (!student.selected) {
            this.setState({selectedStudents: this.state.selectedStudents.filter(i => i!==student.name)});
        } else {
            this.setState({selectedStudents: _.concat(this.state.selectedStudents, student.name)});
        }
        student.selected = !student.selected;
        this.setState({students: this.state.students});
    }
    
    changeStatus = (toStatus = null) => {
        switch (this.state.status) {
            case status.viewing:
                this.setState({status: status.editing});
                break;
            case status.editing:
                this.setState({status: status.saveConfirmingSaving});
                break;
            case status.saveConfirmingSaving:
                this.setState({status: status.absentConfirmingSaving});
                break;
            case status.absentConfirmingSaving:
                this.setState({status: toStatus});
                break;
            default:
                break;
        }
    }
    
    onFinishModal = (isSubmitting, text=null) => {
        this.setState({status: isSubmitting ? status.viewing : status.editing})
    }
    
    renderStudentsStatus() {
        return this.state.students.map(student => {
            return (
                <Grid.Column width={4} key={student.number}>
                    <UserIconWrap>
                        { this.state.status===status.editing? 
                            <Checkbox 
                                className="absent-checkbox" 
                                onChange={() => {this.onStudentAbsentSelected(student.number)}} 
                                checked={student.selected}
                            />    
                            : null }
                        <UserNumber>{student.number}</UserNumber>
                        <UserIconHead className={ (student.selected === true)&&(student.leaveApplied === false)? null: 'absent' }/>
                        <UserIconBody className={ (student.selected === true)&&(student.leaveApplied === false)? null: 'absent' }/>
                        <UserName>{student.name}</UserName>
                    </UserIconWrap>
                    <p className="user-info">{ student.leaveApplied === true? '已請假': null }</p>
                </Grid.Column>);
        });
    }

    render() {
        const editButtonWord = this.state.status===status.editing ? "儲存出缺席" : "編輯出缺席";
        const saveConfirmModal = this.state.status===status.saveConfirmingSaving ? 
            <SaveConFirmModal 
                onFinishModal={this.onFinishModal}
                sendAbsentMessage = { () => { this.changeStatus(status.absentConfirmingSaving) }}
            /> : null;
        const absentConfirmModal = this.state.status===status.absentConfirmingSaving ? 
            <AbsentConFirmModal
                onFinishModal={this.onFinishModal} 
                selectedStudents={this.state.selectedStudents}
            /> : null;
        const studentCount = this.state.status===status.editing ? 
            <Grid.Column width={16}>
                <p>
                    出席： {this.state.students.length - this.state.selectedStudents.length}
                    &emsp;
                    缺席：{this.state.selectedStudents.length}
                </p>
            </Grid.Column> : null;
                
        return (
            <Container className="viewstudents">
                <Grid>
                    <Grid.Column id="upper-buttons" width={16}>
                        <Button compact floated="left" size="tiny">2019 年 1 月 01 日</Button>
                        <Button compact floated="right" size="tiny" basic color="blue" onClick={this.changeStatus} >
                            {editButtonWord}
                        </Button>
                    </Grid.Column>
                    { studentCount }
                    {this.renderStudentsStatus()}
                </Grid>
                { saveConfirmModal }
                { absentConfirmModal }
            </Container>
        );
    }
}

export default ViewStudents;