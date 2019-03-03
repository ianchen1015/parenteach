import React from 'react';
import { Link } from 'react-router-dom';
import { Icon, Menu } from 'semantic-ui-react';

const Header = () => {
    return (
        <Menu inverted icon='labeled' fixed='bottom' color='blue' size='tiny'>
            <Link to="/messages" className="item">
              <Icon name="comments"></Icon>
              訊息管理
            </Link>
            
            <Link to="/students" className="item">
              <Icon name="users"></Icon>
              學生總覽
            </Link>
            
            <Link to="statistics" className="item">
              <Icon name="signal"></Icon>
              統計圖表
            </Link>
            
            <Link to="settings" className="item">
              <Icon name="sliders horizontal"></Icon>
              設定
            </Link>
        </Menu>
    );
};

export default Header;