<?php

/*
*  Copyright (c) C-DAC
*/

class Settings
{

    //////////////////////////////////////////////////////////////////
    // PROPERTIES
    //////////////////////////////////////////////////////////////////

    public $username    = '';
    public $settings    = '';

    //////////////////////////////////////////////////////////////////
    // METHODS
    //////////////////////////////////////////////////////////////////

    // -----------------------------||----------------------------- //

    //////////////////////////////////////////////////////////////////
    // Construct
    //////////////////////////////////////////////////////////////////

    public function __construct()
    {
    }

    //////////////////////////////////////////////////////////////////
    // Save User Settings
    //////////////////////////////////////////////////////////////////

    public function Save()
    {
        if (!file_exists(DATA . "/settings.php")) {
            saveJSON('settings.php', array($this->username => array('codiad.username' => $this->username)));
        }
        $settings = getJSON('settings.php');
        // Security: prevent user side overwritten value
        $this->settings['username'] = $this->username;
        $settings[$this->username] = $this->settings;
        saveJSON('settings.php', $settings);
        echo formatJSEND("success", null);
    }

    //////////////////////////////////////////////////////////////////
    // Load User Settings
    //////////////////////////////////////////////////////////////////

    public function Load()
    {
        if (!file_exists(DATA . "/settings.php")) {
            saveJSON('settings.php', array($this->username => array('codiad.username' => $this->username)));
        }
        $settings = getJSON('settings.php');
        echo formatJSEND("success", $settings[$this->username]);
    }
}
