import React from 'react';
import { Container, Grid, Button, Checkbox } from 'semantic-ui-react';
import _ from 'lodash';

import { UserIconHead, UserName, UserNumber, UserIconBody, UserIconWrap } from './UserStatus';
import ConfirmModal from './ConfirmModal';
import defaultStudents from '../defaultStudents';
import './ViewStudents.css';

const status = {
    viewing: 0,
    editing: 1,
    confirmingSaving: 2,
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
            this.setState({selectedStudents: _.concat(this.state.selectedStudents, student.name)});
        } else {
            this.setState({selectedStudents: this.state.selectedStudents.filter(i => i!==student.name)});
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
                this.setState({status: status.confirmingSaving});
                break;
            case status.confirmingSaving:
                this.setState({status: toStatus});
                break;
            default:
                break;
        }
    }
    
    onFinishModal = (isSubmitting, text=null) => {
        this.changeStatus(isSubmitting ? status.viewing : status.editing);
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
                        <UserIconHead/>
                        <UserIconBody/>
                        <UserName>{student.name}</UserName>
                    </UserIconWrap>
                </Grid.Column>);
        });
    }
    
    render() {
        const editButtonWord = this.state.status===status.editing ? "儲存出缺席" : "編輯出缺席";
        const confirmModal = this.state.status===status.confirmingSaving ? 
            <ConfirmModal 
                onFinishModal={this.onFinishModal} 
                selectedStudents={this.state.selectedStudents}
            /> : null;
                
        return (
            <Container className="viewstudents">
                <Grid>
                    <Grid.Column id="upper-buttons" width={16}>
                        <Button compact floated="left" size="tiny">2019 年 1 月 01 日</Button>
                        <Button compact floated="right" size="tiny" basic color="blue" onClick={this.changeStatus} >
                            {editButtonWord}
                        </Button>
                    </Grid.Column>
                    
                    {this.renderStudentsStatus()}
                </Grid>
                { confirmModal }
            </Container>
        );
    }
}

export default ViewStudents;