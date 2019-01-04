#!/bin/bash

for p in packages/*
  do
    echo $p
    detect-requirements $p
    echo ""
  done

