#!/bin/bash

dpkg --add-architecture i386 && apt update && apt install libssl1.0.0:i386

