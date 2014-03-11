# used for CVS snapshots:
%define CVSDATE %{nil}
%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 0
%endif
%define desktop_file 1
%if %{desktop_file}
%define desktop_file_utils_version 0.2.93
%endif

%define withnetbeans 1

%define withvimspell 0
%define withhunspell 0
%define withruby 1

%define baseversion 7.3
#used for pre-releases:
%define beta %{nil}
%define vimdir vim73%{?beta}
%define patchlevel 969

Summary: The VIM editor
URL:     http://www.vim.org/
Name: vim
Version: %{baseversion}.%{beta}%{patchlevel}
Release: 1%{?dist}
License: Vim
Group: Applications/Editors
Source0: ftp://ftp.vim.org/pub/vim/unix/vim-%{baseversion}%{?beta}%{?CVSDATE}.tar.bz2
Source3: gvim.desktop
Source4: vimrc
Source5: ftp://ftp.vim.org/pub/vim/patches/README.patches
Source7: gvim16.png
Source8: gvim32.png
Source9: gvim48.png
Source10: gvim64.png
Source11: Changelog.rpm
Source12: vi_help.txt
%if %{withvimspell}
Source13: vim-spell-files.tar.bz2
%endif
Source14: spec-template
Source15: spec-template.new
Source16: nl.po

Patch2002: vim-7.0-fixkeys.patch
Patch2003: vim-6.2-specsyntax.patch
Patch2004: vim-7.0-crv.patch
%if %{withhunspell}
Patch2011: vim-7.0-hunspell.patch
BuildRequires: hunspell-devel
%endif
# Patches 001 < 999 are patches from the base maintainer.
# If you're as lazy as me, generate the list using
# for i in `seq 1 14`; do printf "Patch%03d: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.%03d\n" $i $i; done
Patch001: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.001
Patch002: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.002
Patch003: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.003
Patch004: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.004
Patch005: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.005
Patch006: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.006
Patch007: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.007
Patch008: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.008
Patch009: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.009
Patch010: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.010
Patch011: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.011
Patch012: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.012
Patch013: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.013
Patch014: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.014
Patch015: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.015
Patch016: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.016
Patch017: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.017
Patch018: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.018
Patch019: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.019
Patch020: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.020
Patch021: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.021
Patch022: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.022
Patch023: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.023
Patch024: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.024
Patch025: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.025
Patch026: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.026
Patch027: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.027
Patch028: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.028
Patch029: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.029
Patch030: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.030
Patch031: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.031
Patch032: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.032
Patch033: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.033
Patch034: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.034
Patch035: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.035
Patch036: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.036
Patch037: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.037
Patch038: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.038
Patch039: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.039
Patch040: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.040
Patch041: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.041
Patch042: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.042
Patch043: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.043
Patch044: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.044
Patch045: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.045
Patch046: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.046
Patch047: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.047
Patch048: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.048
Patch049: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.049
Patch050: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.050
Patch051: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.051
Patch052: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.052
Patch053: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.053
Patch054: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.054
Patch055: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.055
Patch056: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.056
Patch057: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.057
Patch058: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.058
Patch059: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.059
Patch060: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.060
Patch061: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.061
Patch062: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.062
Patch063: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.063
Patch064: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.064
Patch065: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.065
Patch066: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.066
Patch067: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.067
Patch068: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.068
Patch069: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.069
Patch070: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.070
Patch071: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.071
Patch072: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.072
Patch073: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.073
Patch074: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.074
Patch075: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.075
Patch076: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.076
Patch077: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.077
Patch078: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.078
Patch079: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.079
Patch080: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.080
Patch081: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.081
Patch082: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.082
Patch083: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.083
Patch084: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.084
Patch085: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.085
Patch086: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.086
Patch087: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.087
Patch088: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.088
Patch089: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.089
Patch090: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.090
Patch091: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.091
Patch092: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.092
Patch093: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.093
Patch094: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.094
Patch095: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.095
Patch096: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.096
Patch097: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.097
Patch098: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.098
Patch099: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.099
Patch100: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.100
Patch101: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.101
Patch102: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.102
Patch103: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.103
Patch104: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.104
Patch105: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.105
Patch106: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.106
Patch107: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.107
Patch108: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.108
Patch109: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.109
Patch110: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.110
Patch111: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.111
Patch112: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.112
Patch113: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.113
Patch114: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.114
Patch115: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.115
Patch116: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.116
Patch117: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.117
Patch118: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.118
Patch119: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.119
Patch120: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.120
Patch121: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.121
Patch122: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.122
Patch123: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.123
Patch124: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.124
Patch125: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.125
Patch126: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.126
Patch127: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.127
Patch128: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.128
Patch129: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.129
Patch130: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.130
Patch131: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.131
Patch132: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.132
Patch133: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.133
Patch134: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.134
Patch135: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.135
Patch136: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.136
Patch137: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.137
Patch138: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.138
Patch139: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.139
Patch140: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.140
Patch141: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.141
Patch142: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.142
Patch143: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.143
Patch144: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.144
Patch145: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.145
Patch146: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.146
Patch147: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.147
Patch148: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.148
Patch149: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.149
Patch150: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.150
Patch151: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.151
Patch152: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.152
Patch153: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.153
Patch154: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.154
Patch155: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.155
Patch156: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.156
Patch157: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.157
Patch158: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.158
Patch159: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.159
Patch160: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.160
Patch161: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.161
Patch162: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.162
Patch163: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.163
Patch164: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.164
Patch165: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.165
Patch166: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.166
Patch167: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.167
Patch168: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.168
Patch169: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.169
Patch170: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.170
Patch171: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.171
Patch172: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.172
Patch173: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.173
Patch174: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.174
Patch175: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.175
Patch176: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.176
Patch177: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.177
Patch178: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.178
Patch179: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.179
Patch180: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.180
Patch181: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.181
Patch182: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.182
Patch183: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.183
Patch184: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.184
Patch185: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.185
Patch186: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.186
Patch187: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.187
Patch188: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.188
Patch189: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.189
Patch190: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.190
Patch191: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.191
Patch192: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.192
Patch193: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.193
Patch194: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.194
Patch195: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.195
Patch196: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.196
Patch197: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.197
Patch198: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.198
Patch199: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.199
Patch200: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.200
Patch201: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.201
# Patched:
Patch202: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.202
# Patched:
Patch203: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.203
Patch204: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.204
Patch205: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.205
Patch206: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.206
Patch207: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.207
Patch208: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.208
Patch209: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.209
Patch210: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.210
Patch211: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.211
Patch212: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.212
Patch213: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.213
Patch214: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.214
Patch215: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.215
Patch216: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.216
Patch217: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.217
Patch218: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.218
Patch219: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.219
Patch220: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.220
Patch221: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.221
Patch222: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.222
Patch223: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.223
Patch224: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.224
Patch225: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.225
Patch226: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.226
Patch227: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.227
Patch228: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.228
Patch229: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.229
Patch230: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.230
Patch231: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.231
Patch232: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.232
Patch233: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.233
Patch234: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.234
Patch235: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.235
Patch236: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.236
Patch237: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.237
Patch238: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.238
Patch239: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.239
Patch240: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.240
Patch241: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.241
Patch242: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.242
Patch243: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.243
Patch244: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.244
Patch245: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.245
Patch246: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.246
Patch247: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.247
Patch248: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.248
Patch249: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.249
Patch250: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.250
Patch251: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.251
Patch252: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.252
Patch253: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.253
Patch254: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.254
Patch255: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.255
Patch256: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.256
Patch257: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.257
Patch258: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.258
Patch259: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.259
Patch260: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.260
Patch261: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.261
Patch262: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.262
Patch263: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.263
Patch264: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.264
Patch265: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.265
Patch266: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.266
Patch267: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.267
Patch268: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.268
Patch269: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.269
Patch270: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.270
Patch271: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.271
Patch272: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.272
Patch273: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.273
Patch274: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.274
Patch275: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.275
Patch276: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.276
Patch277: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.277
Patch278: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.278
Patch279: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.279
Patch280: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.280
Patch281: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.281
Patch282: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.282
Patch283: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.283
Patch284: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.284
Patch285: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.285
Patch286: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.286
Patch287: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.287
Patch288: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.288
Patch289: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.289
Patch290: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.290
Patch291: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.291
Patch292: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.292
Patch293: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.293
Patch294: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.294
Patch295: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.295
Patch296: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.296
Patch297: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.297
Patch298: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.298
Patch299: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.299
Patch300: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.300
Patch301: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.301
Patch302: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.302
Patch303: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.303
Patch304: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.304
Patch305: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.305
Patch306: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.306
Patch307: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.307
Patch308: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.308
Patch309: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.309
Patch310: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.310
Patch311: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.311
Patch312: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.312
Patch313: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.313
Patch314: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.314
Patch315: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.315
Patch316: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.316
Patch317: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.317
Patch318: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.318
Patch319: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.319
Patch320: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.320
Patch321: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.321
Patch322: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.322
Patch323: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.323
Patch324: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.324
Patch325: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.325
Patch326: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.326
Patch327: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.327
Patch328: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.328
Patch329: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.329
Patch330: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.330
Patch331: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.331
Patch332: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.332
Patch333: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.333
Patch334: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.334
Patch335: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.335
Patch336: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.336
Patch337: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.337
Patch338: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.338
Patch339: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.339
Patch340: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.340
Patch341: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.341
Patch342: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.342
Patch343: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.343
Patch344: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.344
Patch345: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.345
Patch346: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.346
Patch347: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.347
Patch348: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.348
Patch349: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.349
Patch350: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.350
Patch351: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.351
Patch352: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.352
Patch353: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.353
Patch354: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.354
Patch355: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.355
Patch356: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.356
Patch357: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.357
Patch358: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.358
Patch359: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.359
Patch360: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.360
Patch361: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.361
Patch362: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.362
Patch363: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.363
Patch364: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.364
Patch365: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.365
Patch366: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.366
Patch367: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.367
Patch368: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.368
Patch369: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.369
Patch370: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.370
Patch371: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.371
Patch372: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.372
Patch373: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.373
Patch374: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.374
Patch375: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.375
Patch376: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.376
Patch377: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.377
Patch378: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.378
Patch379: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.379
Patch380: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.380
Patch381: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.381
Patch382: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.382
Patch383: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.383
Patch384: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.384
Patch385: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.385
Patch386: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.386
Patch387: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.387
Patch388: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.388
Patch389: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.389
Patch390: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.390
Patch391: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.391
Patch392: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.392
Patch393: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.393
Patch394: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.394
Patch395: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.395
Patch396: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.396
Patch397: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.397
Patch398: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.398
Patch399: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.399
Patch400: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.400
Patch401: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.401
Patch402: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.402
Patch403: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.403
Patch404: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.404
Patch405: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.405
Patch406: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.406
Patch407: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.407
Patch408: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.408
Patch409: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.409
Patch410: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.410
Patch411: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.411
Patch412: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.412
Patch413: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.413
Patch414: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.414
Patch415: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.415
# Duplicate patch in 427:
#Patch416: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.416
Patch417: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.417
Patch418: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.418
Patch419: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.419
Patch420: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.420
Patch421: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.421
Patch422: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.422
Patch423: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.423
Patch424: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.424
Patch425: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.425
Patch426: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.426
Patch427: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.427
Patch428: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.428
Patch429: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.429
Patch430: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.430
Patch431: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.431
Patch432: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.432
Patch433: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.433
Patch434: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.434
Patch435: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.435
Patch436: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.436
Patch437: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.437
Patch438: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.438
Patch439: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.439
Patch440: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.440
Patch441: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.441
Patch442: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.442
Patch443: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.443
Patch444: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.444
Patch445: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.445
Patch446: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.446
Patch447: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.447
Patch448: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.448
Patch449: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.449
Patch450: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.450
Patch451: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.451
Patch452: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.452
Patch453: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.453
Patch454: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.454
Patch455: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.455
Patch456: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.456
Patch457: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.457
Patch458: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.458
Patch459: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.459
Patch460: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.460
Patch461: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.461
Patch462: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.462
Patch463: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.463
Patch464: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.464
Patch465: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.465
Patch466: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.466
Patch467: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.467
Patch468: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.468
Patch469: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.469
Patch470: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.470
Patch471: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.471
Patch472: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.472
Patch473: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.473
Patch474: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.474
Patch475: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.475
Patch476: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.476
Patch477: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.477
Patch478: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.478
Patch479: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.479
Patch480: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.480
Patch481: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.481
Patch482: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.482
Patch483: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.483
Patch484: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.484
Patch485: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.485
Patch486: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.486
Patch487: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.487
Patch488: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.488
Patch489: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.489
Patch490: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.490
Patch491: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.491
Patch492: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.492
Patch493: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.493
Patch494: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.494
Patch495: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.495
Patch496: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.496
Patch497: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.497
Patch498: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.498
Patch499: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.499
Patch500: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.500
Patch501: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.501
Patch502: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.502
Patch503: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.503
Patch504: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.504
Patch505: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.505
Patch506: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.506
Patch507: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.507
Patch508: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.508
Patch509: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.509
Patch510: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.510
Patch511: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.511
Patch512: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.512
Patch513: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.513
Patch514: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.514
Patch515: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.515
Patch516: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.516
Patch517: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.517
Patch518: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.518
Patch519: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.519
Patch520: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.520
Patch521: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.521
Patch522: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.522
Patch523: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.523
Patch524: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.524
Patch525: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.525
Patch526: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.526
Patch527: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.527
Patch528: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.528
Patch529: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.529
Patch530: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.530
Patch531: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.531
Patch532: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.532
Patch533: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.533
Patch534: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.534
Patch535: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.535
Patch536: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.536
Patch537: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.537
Patch538: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.538
Patch539: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.539
Patch540: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.540
Patch541: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.541
Patch542: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.542
Patch543: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.543
Patch544: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.544
Patch545: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.545
Patch546: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.546
Patch547: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.547
Patch548: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.548
Patch549: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.549
Patch550: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.550
Patch551: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.551
Patch552: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.552
Patch553: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.553
Patch554: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.554
Patch555: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.555
Patch556: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.556
Patch557: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.557
Patch558: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.558
Patch559: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.559
Patch560: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.560
Patch561: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.561
Patch562: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.562
Patch563: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.563
Patch564: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.564
Patch565: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.565
Patch566: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.566
Patch567: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.567
Patch568: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.568
Patch569: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.569
Patch570: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.570
Patch571: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.571
Patch572: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.572
Patch573: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.573
Patch574: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.574
Patch575: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.575
Patch576: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.576
Patch577: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.577
Patch578: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.578
Patch579: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.579
Patch580: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.580
Patch581: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.581
Patch582: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.582
Patch583: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.583
Patch584: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.584
Patch585: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.585
Patch586: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.586
Patch587: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.587
Patch588: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.588
Patch589: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.589
Patch590: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.590
Patch591: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.591
Patch592: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.592
Patch593: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.593
Patch594: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.594
Patch595: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.595
Patch596: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.596
Patch597: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.597
Patch598: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.598
Patch599: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.599
Patch600: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.600
Patch601: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.601
Patch602: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.602
Patch603: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.603
Patch604: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.604
Patch605: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.605
Patch606: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.606
Patch607: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.607
Patch608: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.608
Patch609: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.609
Patch610: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.610
Patch611: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.611
Patch612: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.612
Patch613: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.613
Patch614: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.614
Patch615: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.615
Patch616: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.616
Patch617: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.617
Patch618: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.618
Patch619: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.619
Patch620: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.620
Patch621: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.621
Patch622: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.622
Patch623: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.623
Patch624: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.624
Patch625: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.625
Patch626: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.626
Patch627: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.627
Patch628: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.628
Patch629: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.629
Patch630: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.630
Patch631: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.631
Patch632: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.632
Patch633: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.633
Patch634: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.634
Patch635: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.635
Patch636: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.636
Patch637: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.637
Patch638: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.638
Patch639: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.639
Patch640: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.640
Patch641: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.641
Patch642: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.642
Patch643: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.643
Patch644: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.644
Patch645: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.645
Patch646: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.646
Patch647: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.647
Patch648: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.648
Patch649: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.649
Patch650: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.650
Patch651: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.651
Patch652: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.652
Patch653: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.653
Patch654: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.654
Patch655: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.655
Patch656: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.656
Patch657: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.657
Patch658: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.658
Patch659: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.659
Patch660: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.660
Patch661: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.661
Patch662: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.662
Patch663: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.663
Patch664: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.664
Patch665: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.665
Patch666: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.666
Patch667: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.667
Patch668: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.668
Patch669: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.669
Patch670: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.670
Patch671: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.671
Patch672: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.672
Patch673: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.673
Patch674: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.674
Patch675: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.675
Patch676: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.676
Patch677: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.677
Patch678: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.678
Patch679: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.679
Patch680: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.680
Patch681: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.681
Patch682: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.682
Patch683: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.683
Patch684: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.684
Patch685: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.685
Patch686: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.686
Patch687: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.687
Patch688: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.688
Patch689: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.689
Patch690: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.690
Patch691: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.691
Patch692: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.692
Patch693: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.693
Patch694: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.694
Patch695: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.695
Patch696: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.696
Patch697: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.697
Patch698: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.698
Patch699: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.699
Patch700: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.700
Patch701: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.701
Patch702: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.702
Patch703: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.703
Patch704: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.704
Patch705: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.705
Patch706: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.706
Patch707: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.707
Patch708: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.708
Patch709: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.709
Patch710: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.710
Patch711: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.711
Patch712: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.712
Patch713: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.713
Patch714: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.714
Patch715: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.715
Patch716: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.716
Patch717: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.717
Patch718: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.718
Patch719: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.719
Patch720: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.720
Patch721: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.721
Patch722: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.722
Patch723: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.723
Patch724: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.724
Patch725: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.725
Patch726: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.726
Patch727: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.727
Patch728: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.728
Patch729: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.729
Patch730: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.730
Patch731: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.731
Patch732: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.732
Patch733: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.733
Patch734: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.734
Patch735: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.735
Patch736: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.736
Patch737: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.737
Patch738: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.738
Patch739: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.739
Patch740: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.740
Patch741: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.741
Patch742: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.742
Patch743: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.743
Patch744: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.744
Patch745: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.745
Patch746: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.746
Patch747: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.747
Patch748: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.748
Patch749: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.749
Patch750: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.750
Patch751: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.751
Patch752: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.752
Patch753: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.753
Patch754: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.754
Patch755: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.755
Patch756: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.756
Patch757: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.757
Patch758: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.758
Patch759: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.759
Patch760: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.760
Patch761: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.761
Patch762: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.762
Patch763: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.763
Patch764: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.764
Patch765: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.765
Patch766: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.766
Patch767: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.767
Patch768: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.768
Patch769: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.769
Patch770: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.770
Patch771: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.771
Patch772: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.772
Patch773: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.773
Patch774: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.774
Patch775: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.775
Patch776: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.776
Patch777: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.777
Patch778: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.778
Patch779: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.779
Patch780: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.780
Patch781: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.781
Patch782: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.782
Patch783: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.783
Patch784: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.784
Patch785: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.785
Patch786: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.786
Patch787: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.787
Patch788: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.788
Patch789: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.789
Patch790: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.790
Patch791: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.791
Patch792: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.792
Patch793: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.793
Patch794: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.794
Patch795: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.795
Patch796: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.796
Patch797: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.797
Patch798: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.798
Patch799: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.799
Patch800: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.800
Patch801: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.801
Patch802: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.802
Patch803: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.803
Patch804: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.804
Patch805: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.805
Patch806: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.806
Patch807: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.807
Patch808: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.808
Patch809: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.809
Patch810: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.810
Patch811: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.811
Patch812: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.812
Patch813: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.813
Patch814: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.814
Patch815: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.815
Patch816: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.816
Patch817: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.817
Patch818: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.818
Patch819: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.819
Patch820: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.820
Patch821: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.821
Patch822: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.822
Patch823: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.823
Patch824: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.824
Patch825: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.825
Patch826: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.826
Patch827: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.827
Patch828: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.828
Patch829: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.829
Patch830: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.830
Patch831: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.831
Patch832: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.832
Patch833: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.833
Patch834: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.834
Patch835: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.835
Patch836: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.836
Patch837: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.837
Patch838: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.838
Patch839: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.839
Patch840: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.840
Patch841: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.841
Patch842: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.842
Patch843: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.843
Patch844: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.844
Patch845: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.845
Patch846: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.846
Patch847: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.847
Patch848: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.848
Patch849: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.849
Patch850: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.850
Patch851: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.851
Patch852: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.852
Patch853: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.853
Patch854: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.854
Patch855: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.855
Patch856: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.856
Patch857: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.857
Patch858: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.858
Patch859: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.859
Patch860: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.860
Patch861: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.861
Patch862: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.862
Patch863: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.863
Patch864: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.864
Patch865: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.865
Patch866: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.866
Patch867: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.867
Patch868: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.868
Patch869: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.869
Patch870: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.870
Patch871: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.871
Patch872: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.872
Patch873: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.873
Patch874: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.874
Patch875: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.875
Patch876: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.876
Patch877: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.877
Patch878: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.878
Patch879: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.879
Patch880: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.880
Patch881: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.881
Patch882: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.882
Patch883: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.883
Patch884: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.884
Patch885: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.885
Patch886: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.886
Patch887: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.887
Patch888: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.888
Patch889: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.889
Patch890: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.890
Patch891: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.891
Patch892: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.892
Patch893: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.893
Patch894: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.894
Patch895: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.895
Patch896: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.896
Patch897: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.897
Patch898: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.898
Patch899: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.899
Patch900: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.900
Patch901: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.901
Patch902: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.902
Patch903: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.903
Patch904: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.904
Patch905: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.905
Patch906: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.906
Patch907: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.907
Patch908: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.908
Patch909: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.909
Patch910: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.910
Patch911: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.911
Patch912: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.912
Patch913: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.913
Patch914: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.914
Patch915: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.915
Patch916: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.916
Patch917: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.917
Patch918: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.918
Patch919: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.919
Patch920: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.920
Patch921: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.921
Patch922: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.922
Patch923: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.923
Patch924: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.924
Patch925: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.925
Patch926: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.926
Patch927: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.927
Patch928: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.928
Patch929: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.929
Patch930: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.930
Patch931: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.931
Patch932: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.932
Patch933: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.933
Patch934: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.934
Patch935: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.935
Patch936: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.936
Patch937: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.937
Patch938: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.938
Patch939: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.939
Patch940: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.940
Patch941: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.941
Patch942: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.942
Patch943: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.943
Patch944: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.944
Patch945: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.945
Patch946: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.946
Patch947: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.947
Patch948: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.948
Patch949: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.949
Patch950: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.950
Patch951: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.951
Patch952: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.952
Patch953: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.953
Patch954: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.954
Patch955: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.955
Patch956: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.956
Patch957: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.957
Patch958: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.958
Patch959: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.959
Patch960: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.960
Patch961: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.961
Patch962: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.962
Patch963: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.963
Patch964: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.964
Patch965: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.965
Patch966: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.966
Patch967: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.967
Patch968: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.968
Patch969: ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.969

Patch3000: vim-7.3-syntax.patch
Patch3002: vim-7.1-nowarnings.patch
Patch3004: vim-7.0-rclocation.patch
Patch3006: vim-6.4-checkhl.patch
Patch3007: vim-7.3-fstabsyntax.patch
Patch3008: vim-7.0-warning.patch
Patch3009: vim-7.0-syncolor.patch
Patch3010: vim-7.0-specedit.patch
Patch3011: vim72-rh514717.patch
Patch3012: vim-7.3-bug816848.patch
Patch3013: vim-7.3-manpage-typo-668894-675480.patch
Patch3014: vim-ruby20.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel ncurses-devel gettext perl-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: libacl-devel gpm-devel autoconf
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
%if "%{withruby}" == "1"
Buildrequires: ruby-devel ruby
%endif
%if %{desktop_file}
# for /usr/bin/desktop-file-install
Requires: desktop-file-utils
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
%endif
Epoch: 2
Conflicts: filesystem < 3

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor
Group: Applications/Editors
Conflicts: man-pages-fr < 0.9.7-14
Conflicts: man-pages-it < 0.3.0-17
Conflicts: man-pages-pl < 0.24-2
Requires: %{name}-filesystem

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.

%package spell
Summary: The dictionaries for spell checking. This package is optional
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release}

%description spell
This subpackage contains dictionaries for vim spell checking in
many different languages.

%package minimal
Summary: A minimal version of the VIM editor
Group: Applications/Editors
Provides: vi = %{version}-%{release}
Provides: /bin/vi

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.

%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} which
Provides: vim = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.

%package filesystem
Summary: VIM filesystem layout
Group: Applications/Editors

%Description filesystem
This package provides some directories which are required by other
packages that add vim files, p.e.  additional syntax files or filetypes.

%package X11
Summary: The VIM version of the vi editor for the X Window System
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} libattr >= 2.4 gtk2 >= 2.6
Provides: gvim = %{version}-%{release}
BuildRequires: gtk2-devel libSM-devel libXt-devel libXpm-devel
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: hicolor-icon-theme

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.

%prep
%setup -q -b 0 -n %{vimdir}
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
%patch2002 -p1
%patch2003 -p1
%patch2004 -p1
%if %{withhunspell}
%patch2011 -p1
%endif
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

# Base patches...
# for i in `seq 1 14`; do printf "%%patch%03d -p0 \n" $i; done
%patch001 -p0
%patch002 -p0
%patch003 -p0
%patch004 -p0
%patch005 -p0
%patch006 -p0
%patch007 -p0
%patch008 -p0
%patch009 -p0
%patch010 -p0
%patch011 -p0
%patch012 -p0
%patch013 -p0
%patch014 -p0
%patch015 -p0
%patch016 -p0
%patch017 -p0
%patch018 -p0
%patch019 -p0
%patch020 -p0
%patch021 -p0
%patch022 -p0
%patch023 -p0
%patch024 -p0
%patch025 -p0
%patch026 -p0
%patch027 -p0
%patch028 -p0
%patch029 -p0
%patch030 -p0
%patch031 -p0
%patch032 -p0
%patch033 -p0
%patch034 -p0
%patch035 -p0
%patch036 -p0
%patch037 -p0
%patch038 -p0
%patch039 -p0
%patch040 -p0
%patch041 -p0
%patch042 -p0
%patch043 -p0
%patch044 -p0
%patch045 -p0
%patch046 -p0
%patch047 -p0
%patch048 -p0
%patch049 -p0
%patch050 -p0
%patch051 -p0
%patch052 -p0
%patch053 -p0
%patch054 -p0
%patch055 -p0
%patch056 -p0
%patch057 -p0
%patch058 -p0
%patch059 -p0
%patch060 -p0
%patch061 -p0
%patch062 -p0
%patch063 -p0
%patch064 -p0
%patch065 -p0
%patch066 -p0
%patch067 -p0
%patch068 -p0
%patch069 -p0
%patch070 -p0
%patch071 -p0
%patch072 -p0
%patch073 -p0
%patch074 -p0
%patch075 -p0
%patch076 -p0
%patch077 -p0
%patch078 -p0
%patch079 -p0
%patch080 -p0
%patch081 -p0
%patch082 -p0
%patch083 -p0
%patch084 -p0
%patch085 -p0
%patch086 -p0
%patch087 -p0
%patch088 -p0
%patch089 -p0
%patch090 -p0
%patch091 -p0
%patch092 -p0
%patch093 -p0
%patch094 -p0
%patch095 -p0
%patch096 -p0
%patch097 -p0
%patch098 -p0
%patch099 -p0
%patch100 -p0
%patch101 -p0
%patch102 -p0
%patch103 -p0
%patch104 -p0
%patch105 -p0
%patch106 -p0
%patch107 -p0
%patch108 -p0
%patch109 -p0
%patch110 -p0
%patch111 -p0
%patch112 -p0
%patch113 -p0
%patch114 -p0
%patch115 -p0
%patch116 -p0
%patch117 -p0
%patch118 -p0
%patch119 -p0
%patch120 -p0
%patch121 -p0
%patch122 -p0
%patch123 -p0
%patch124 -p0
%patch125 -p0
%patch126 -p0
%patch127 -p0
%patch128 -p0
%patch129 -p0
%patch130 -p0
%patch131 -p0
%patch132 -p0
%patch133 -p0
%patch134 -p0
%patch135 -p0
%patch136 -p0
%patch137 -p0
%patch138 -p0
%patch139 -p0
%patch140 -p0
%patch141 -p0
%patch142 -p0
%patch143 -p0
%patch144 -p0
%patch145 -p0
%patch146 -p0
%patch147 -p0
%patch148 -p0
%patch149 -p0
%patch150 -p0
%patch151 -p0
%patch152 -p0
%patch153 -p0
%patch154 -p0
%patch155 -p0
%patch156 -p0
%patch157 -p0
%patch158 -p0
%patch159 -p0
%patch160 -p0
%patch161 -p0
%patch162 -p0
%patch163 -p0
%patch164 -p0
%patch165 -p0
%patch166 -p0
%patch167 -p0
%patch168 -p0
%patch169 -p0
%patch170 -p0
%patch171 -p0
%patch172 -p0
%patch173 -p0
%patch174 -p0
%patch175 -p0
%patch176 -p0
%patch177 -p0
%patch178 -p0
%patch179 -p0
%patch180 -p0
%patch181 -p0
%patch182 -p0
%patch183 -p0
%patch184 -p0
%patch185 -p0
%patch186 -p0
%patch187 -p0
%patch188 -p0
%patch189 -p0
%patch190 -p0
%patch191 -p0
%patch192 -p0
%patch193 -p0
%patch194 -p0
%patch195 -p0
%patch196 -p0
%patch197 -p0
%patch198 -p0
%patch199 -p0
%patch200 -p0
%patch201 -p0
%patch202 -p0
%patch203 -p0
%patch204 -p0
%patch205 -p0
%patch206 -p0
%patch207 -p0
%patch208 -p0
%patch209 -p0
%patch210 -p0
%patch211 -p0
%patch212 -p0
%patch213 -p0
%patch214 -p0
%patch215 -p0
%patch216 -p0
%patch217 -p0
%patch218 -p0
%patch219 -p0
%patch220 -p0
%patch221 -p0
%patch222 -p0
%patch223 -p0
%patch224 -p0
%patch225 -p0
%patch226 -p0
%patch227 -p0
%patch228 -p0
%patch229 -p0
%patch230 -p0
%patch231 -p0
%patch232 -p0
%patch233 -p0
%patch234 -p0
%patch235 -p0
%patch236 -p0
%patch237 -p0
%patch238 -p0
%patch239 -p0
%patch240 -p0
%patch241 -p0
%patch242 -p0
%patch243 -p0
%patch244 -p0
%patch245 -p0
%patch246 -p0
%patch247 -p0
%patch248 -p0
%patch249 -p0
%patch250 -p0
%patch251 -p0
%patch252 -p0
%patch253 -p0
%patch254 -p0
%patch255 -p0
%patch256 -p0
%patch257 -p0
%patch258 -p0
%patch259 -p0
%patch260 -p0
%patch261 -p0
%patch262 -p0
%patch263 -p0
%patch264 -p0
%patch265 -p0
%patch266 -p0
%patch267 -p0
%patch268 -p0
%patch269 -p0
%patch270 -p0
%patch271 -p0
%patch272 -p0
%patch273 -p0
%patch274 -p0
%patch275 -p0
%patch276 -p0
%patch277 -p0
%patch278 -p0
%patch279 -p0
%patch280 -p0
%patch281 -p0
%patch282 -p0
%patch283 -p0
%patch284 -p0
%patch285 -p0
%patch286 -p0
%patch287 -p0
%patch288 -p0
%patch289 -p0
%patch290 -p0
%patch291 -p0
%patch292 -p0
%patch293 -p0
%patch294 -p0
%patch295 -p0
%patch296 -p0
%patch297 -p0
%patch298 -p0
%patch299 -p0
%patch300 -p0
%patch301 -p0
%patch302 -p0
%patch303 -p0
%patch304 -p0
%patch305 -p0
%patch306 -p0
%patch307 -p0
%patch308 -p0
%patch309 -p0
%patch310 -p0
%patch311 -p0
%patch312 -p0
%patch313 -p0
%patch314 -p0
%patch315 -p0
%patch316 -p0
%patch317 -p0
%patch318 -p0
%patch319 -p0
%patch320 -p0
%patch321 -p0
%patch322 -p0
%patch323 -p0
%patch324 -p0
%patch325 -p0
%patch326 -p0
%patch327 -p0
%patch328 -p0
%patch329 -p0
%patch330 -p0
%patch331 -p0
%patch332 -p0
%patch333 -p0
%patch334 -p0
%patch335 -p0
%patch336 -p0
%patch337 -p0
%patch338 -p0
%patch339 -p0
%patch340 -p0
%patch341 -p0
%patch342 -p0
%patch343 -p0
%patch344 -p0
%patch345 -p0
%patch346 -p0
%patch347 -p0
%patch348 -p0
%patch349 -p0
%patch350 -p0
%patch351 -p0
%patch352 -p0
%patch353 -p0
%patch354 -p0
%patch355 -p0
%patch356 -p0
%patch357 -p0
%patch358 -p0
%patch359 -p0
%patch360 -p0
%patch361 -p0
%patch362 -p0
%patch363 -p0
%patch364 -p0
%patch365 -p0
%patch366 -p0
%patch367 -p0
%patch368 -p0
%patch369 -p0
%patch370 -p0
%patch371 -p0
%patch372 -p0
%patch373 -p0
%patch374 -p0
%patch375 -p0
%patch376 -p0
%patch377 -p0
%patch378 -p0
%patch379 -p0
%patch380 -p0
%patch381 -p0
%patch382 -p0
%patch383 -p0
%patch384 -p0
%patch385 -p0
%patch386 -p0
%patch387 -p0
%patch388 -p0
%patch389 -p0
%patch390 -p0
%patch391 -p0
%patch392 -p0
%patch393 -p0
%patch394 -p0
%patch395 -p0
%patch396 -p0
%patch397 -p0
%patch398 -p0
%patch399 -p0
%patch400 -p0
%patch401 -p0
%patch402 -p0
%patch403 -p0
%patch404 -p0
%patch405 -p0
%patch406 -p0
%patch407 -p0
%patch408 -p0
%patch409 -p0
%patch410 -p0
%patch411 -p0
%patch412 -p0
%patch413 -p0
%patch414 -p0
%patch415 -p0
# Duplicate patch in 427:
#patch416 -p0
%patch417 -p0
%patch418 -p0
%patch419 -p0
%patch420 -p0
%patch421 -p0
%patch422 -p0
%patch423 -p0
%patch424 -p0
%patch425 -p0
%patch426 -p0
%patch427 -p0
%patch428 -p0
%patch429 -p0
%patch430 -p0
%patch431 -p0
%patch432 -p0
%patch433 -p0
%patch434 -p0
%patch435 -p0
%patch436 -p0
%patch437 -p0
%patch438 -p0
%patch439 -p0
%patch440 -p0
%patch441 -p0
%patch442 -p0
%patch443 -p0
%patch444 -p0
%patch445 -p0
%patch446 -p0
%patch447 -p0
%patch448 -p0
%patch449 -p0
%patch450 -p0
%patch451 -p0
%patch452 -p0
%patch453 -p0
%patch454 -p0
%patch455 -p0
%patch456 -p0
%patch457 -p0
%patch458 -p0
%patch459 -p0
%patch460 -p0
%patch461 -p0
%patch462 -p0
%patch463 -p0
%patch464 -p0
%patch465 -p0
%patch466 -p0
%patch467 -p0
%patch468 -p0
%patch469 -p0
%patch470 -p0
%patch471 -p0
%patch472 -p0
%patch473 -p0
%patch474 -p0
%patch475 -p0
%patch476 -p0
%patch477 -p0
%patch478 -p0
%patch479 -p0
%patch480 -p0
%patch481 -p0
%patch482 -p0
%patch483 -p0
%patch484 -p0
%patch485 -p0
%patch486 -p0
%patch487 -p0
%patch488 -p0
%patch489 -p0
%patch490 -p0
%patch491 -p0
%patch492 -p0
%patch493 -p0
%patch494 -p0
%patch495 -p0
%patch496 -p0
%patch497 -p0
%patch498 -p0
%patch499 -p0
%patch500 -p0
%patch501 -p0
%patch502 -p0
%patch503 -p0
%patch504 -p0
%patch505 -p0
%patch506 -p0
%patch507 -p0
%patch508 -p0
%patch509 -p0
%patch510 -p0
%patch511 -p0
%patch512 -p0
%patch513 -p0
%patch514 -p0
%patch515 -p0
%patch516 -p0
%patch517 -p0
%patch518 -p0
%patch519 -p0
%patch520 -p0
%patch521 -p0
%patch522 -p0
%patch523 -p0
%patch524 -p0
%patch525 -p0
%patch526 -p0
%patch527 -p0
%patch528 -p0
%patch529 -p0
%patch530 -p0
%patch531 -p0
%patch532 -p0
%patch533 -p0
%patch534 -p0
%patch535 -p0
%patch536 -p0
%patch537 -p0
%patch538 -p0
%patch539 -p0
%patch540 -p0
%patch541 -p0
%patch542 -p0
%patch543 -p0
%patch544 -p0
%patch545 -p0
%patch546 -p0
%patch547 -p0
%patch548 -p0
%patch549 -p0
%patch550 -p0
%patch551 -p0
%patch552 -p0
%patch553 -p0
%patch554 -p0
%patch555 -p0
%patch556 -p0
%patch557 -p0
%patch558 -p0
%patch559 -p0
%patch560 -p0
%patch561 -p0
%patch562 -p0
%patch563 -p0
%patch564 -p0
%patch565 -p0
%patch566 -p0
%patch567 -p0
%patch568 -p0
%patch569 -p0
%patch570 -p0
%patch571 -p0
%patch572 -p0
%patch573 -p0
%patch574 -p0
%patch575 -p0
%patch576 -p0
%patch577 -p0
%patch578 -p0
%patch579 -p0
%patch580 -p0
%patch581 -p0
%patch582 -p0
%patch583 -p0
%patch584 -p0
%patch585 -p0
%patch586 -p0
%patch587 -p0
%patch588 -p0
%patch589 -p0
%patch590 -p0
%patch591 -p0
%patch592 -p0
%patch593 -p0
%patch594 -p0
%patch595 -p0
%patch596 -p0
%patch597 -p0
%patch598 -p0
%patch599 -p0
%patch600 -p0
%patch601 -p0
%patch602 -p0
%patch603 -p0
%patch604 -p0
%patch605 -p0
%patch606 -p0
%patch607 -p0
%patch608 -p0
%patch609 -p0
%patch610 -p0
%patch611 -p0
%patch612 -p0
%patch613 -p0
%patch614 -p0
%patch615 -p0
%patch616 -p0
%patch617 -p0
%patch618 -p0
%patch619 -p0
%patch620 -p0
%patch621 -p0
%patch622 -p0
%patch623 -p0
%patch624 -p0
%patch625 -p0
%patch626 -p0
%patch627 -p0
%patch628 -p0
%patch629 -p0
%patch630 -p0
%patch631 -p0
%patch632 -p0
%patch633 -p0
%patch634 -p0
%patch635 -p0
%patch636 -p0
%patch637 -p0
%patch638 -p0
%patch639 -p0
%patch640 -p0
%patch641 -p0
%patch642 -p0
%patch643 -p0
%patch644 -p0
%patch645 -p0
%patch646 -p0
%patch647 -p0
%patch648 -p0
%patch649 -p0
%patch650 -p0
%patch651 -p0
%patch652 -p0
%patch653 -p0
%patch654 -p0
%patch655 -p0
%patch656 -p0
%patch657 -p0
%patch658 -p0
%patch659 -p0
%patch660 -p0
%patch661 -p0
%patch662 -p0
%patch663 -p0
%patch664 -p0
%patch665 -p0
%patch666 -p0
%patch667 -p0
%patch668 -p0
%patch669 -p0
%patch670 -p0
%patch671 -p0
%patch672 -p0
%patch673 -p0
%patch674 -p0
%patch675 -p0
%patch676 -p0
%patch677 -p0
%patch678 -p0
%patch679 -p0
%patch680 -p0
%patch681 -p0
%patch682 -p0
%patch683 -p0
%patch684 -p0
%patch685 -p0
%patch686 -p0
%patch687 -p0
%patch688 -p0
%patch689 -p0
%patch690 -p0
%patch691 -p0
%patch692 -p0
%patch693 -p0
%patch694 -p0
%patch695 -p0
%patch696 -p0
%patch697 -p0
%patch698 -p0
%patch699 -p0
%patch700 -p0
%patch701 -p0
%patch702 -p0
%patch703 -p0
%patch704 -p0
%patch705 -p0
%patch706 -p0
%patch707 -p0
%patch708 -p0
%patch709 -p0
%patch710 -p0
%patch711 -p0
%patch712 -p0
%patch713 -p0
%patch714 -p0
%patch715 -p0
%patch716 -p0
%patch717 -p0
%patch718 -p0
%patch719 -p0
%patch720 -p0
%patch721 -p0
%patch722 -p0
%patch723 -p0
%patch724 -p0
%patch725 -p0
%patch726 -p0
%patch727 -p0
%patch728 -p0
%patch729 -p0
%patch730 -p0
%patch731 -p0
%patch732 -p0
%patch733 -p0
%patch734 -p0
%patch735 -p0
%patch736 -p0
%patch737 -p0
%patch738 -p0
%patch739 -p0
%patch740 -p0
%patch741 -p0
%patch742 -p0
%patch743 -p0
%patch744 -p0
%patch745 -p0
%patch746 -p0
%patch747 -p0
%patch748 -p0
%patch749 -p0
%patch750 -p0
%patch751 -p0
%patch752 -p0
%patch753 -p0
%patch754 -p0
%patch755 -p0
%patch756 -p0
%patch757 -p0
%patch758 -p0
%patch759 -p0
%patch760 -p0
%patch761 -p0
%patch762 -p0
%patch763 -p0
%patch764 -p0
%patch765 -p0
%patch766 -p0
%patch767 -p0
%patch768 -p0
%patch769 -p0
%patch770 -p0
%patch771 -p0
%patch772 -p0
%patch773 -p0
%patch774 -p0
%patch775 -p0
%patch776 -p0
%patch777 -p0
%patch778 -p0
%patch779 -p0
%patch780 -p0
%patch781 -p0
%patch782 -p0
%patch783 -p0
%patch784 -p0
%patch785 -p0
%patch786 -p0
%patch787 -p0
%patch788 -p0
%patch789 -p0
%patch790 -p0
%patch791 -p0
%patch792 -p0
%patch793 -p0
%patch794 -p0
%patch795 -p0
%patch796 -p0
%patch797 -p0
%patch798 -p0
%patch799 -p0
%patch800 -p0
%patch801 -p0
%patch802 -p0
%patch803 -p0
%patch804 -p0
%patch805 -p0
%patch806 -p0
%patch807 -p0
%patch808 -p0
%patch809 -p0
%patch810 -p0
%patch811 -p0
%patch812 -p0
%patch813 -p0
%patch814 -p0
%patch815 -p0
%patch816 -p0
%patch817 -p0
%patch818 -p0
%patch819 -p0
%patch820 -p0
%patch821 -p0
%patch822 -p0
%patch823 -p0
%patch824 -p0
%patch825 -p0
%patch826 -p0
%patch827 -p0
%patch828 -p0
%patch829 -p0
%patch830 -p0
%patch831 -p0
%patch832 -p0
%patch833 -p0
%patch834 -p0
%patch835 -p0
%patch836 -p0
%patch837 -p0
%patch838 -p0
%patch839 -p0
%patch840 -p0
%patch841 -p0
%patch842 -p0
%patch843 -p0
%patch844 -p0
%patch845 -p0
%patch846 -p0
%patch847 -p0
%patch848 -p0
%patch849 -p0
%patch850 -p0
%patch851 -p0
%patch852 -p0
%patch853 -p0
%patch854 -p0
%patch855 -p0
%patch856 -p0
%patch857 -p0
%patch858 -p0
#%patch859 -p0
%patch860 -p0
%patch861 -p0
%patch862 -p0
#%patch863 -p0
%patch864 -p0
%patch865 -p0
%patch866 -p0
%patch867 -p0
%patch868 -p0
%patch869 -p0
%patch870 -p0
%patch871 -p0
%patch872 -p0
%patch873 -p0
%patch874 -p0
%patch875 -p0
%patch876 -p0
%patch877 -p0
%patch878 -p0
%patch879 -p0
%patch880 -p0
%patch881 -p0
#%patch882 -p0
%patch883 -p0
#%patch884 -p0
%patch885 -p0
%patch886 -p0
%patch887 -p0
%patch888 -p0
%patch889 -p0
%patch890 -p0
%patch891 -p0
%patch892 -p0
%patch893 -p0
%patch894 -p0
%patch895 -p0
%patch896 -p0
%patch897 -p0
%patch898 -p0
%patch899 -p0
%patch900 -p0
%patch901 -p0
%patch902 -p0
%patch903 -p0
%patch904 -p0
%patch905 -p0
%patch906 -p0
%patch907 -p0
%patch908 -p0
%patch909 -p0
%patch910 -p0
%patch911 -p0
%patch912 -p0
%patch913 -p0
%patch914 -p0
%patch915 -p0
%patch916 -p0
%patch917 -p0
%patch918 -p0
%patch919 -p0
%patch920 -p0
%patch921 -p0
%patch922 -p0
%patch923 -p0
%patch924 -p0
%patch925 -p0
%patch926 -p0
%patch927 -p0
%patch928 -p0
%patch929 -p0
%patch930 -p0
%patch931 -p0
%patch932 -p0
%patch933 -p0
%patch934 -p0
%patch935 -p0
%patch936 -p0
%patch937 -p0
%patch938 -p0
%patch939 -p0
%patch940 -p0
%patch941 -p0
%patch942 -p0
%patch943 -p0
#%patch944 -p0
%patch945 -p0
#%patch946 -p0
%patch947 -p0
%patch948 -p0
%patch949 -p0
%patch950 -p0
%patch951 -p0
%patch952 -p0
%patch953 -p0
%patch954 -p0
%patch955 -p0
%patch956 -p0
%patch957 -p0
%patch958 -p0
%patch959 -p0
%patch960 -p0
%patch961 -p0
%patch962 -p0
%patch963 -p0
%patch964 -p0
%patch965 -p0
%patch966 -p0
%patch967 -p0
%patch968 -p0
%patch969 -p0

# install spell files
%if %{withvimspell}
%{__tar} xjf %{SOURCE13}
%endif

%patch3000 -p1
%patch3002 -p1
%patch3004 -p1
%patch3006 -p1
%patch3007 -p1
%patch3008 -p1
%patch3009 -p1
%patch3010 -p1
%patch3011 -p1
%patch3012 -p1
%patch3013 -p1
%patch3014 -p1

%build
cp -f %{SOURCE5} .
cp -f %{SOURCE16} src/po/
cd src
autoconf

sed -e "s+VIMRCLOC	= \$(VIMLOC)+VIMRCLOC	= /etc+" Makefile > Makefile.tmp
mv -f Makefile.tmp Makefile

export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"

%configure --with-features=huge \
  --enable-pythoninterp=dynamic \
  --enable-perlinterp \
  --disable-tclinterp --with-x=yes \
  --enable-xim --enable-multibyte \
  --with-tlib=ncurses \
  --enable-gtk2-check --enable-gui=gtk2 \
  --with-compiledby="<bugzilla@redhat.com>" --enable-cscope \
  --with-modified-by="<bugzilla@redhat.com>" \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp=dynamic \
%else
  --disable-rubyinterp \
%endif

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim gvim
make clean

%configure --prefix=%{_prefix} --with-features=huge \
 --enable-pythoninterp=dynamic \
 --enable-perlinterp \
 --disable-tclinterp \
 --with-x=no \
 --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
 --enable-cscope --with-modified-by="<bugzilla@redhat.com>" \
 --with-tlib=ncurses \
 --with-compiledby="<bugzilla@redhat.com>" \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp=dynamic \
%else
  --disable-rubyinterp \
%endif

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim enhanced-vim
make clean

perl -pi -e "s/help.txt/vi_help.txt/"  os_unix.h ex_cmds.c
perl -pi -e "s/\/etc\/vimrc/\/etc\/virc/"  os_unix.h
%configure --prefix=%{_prefix} --with-features=small --with-x=no \
  --enable-multibyte \
  --disable-netbeans \
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
  --disable-pythoninterp --disable-perlinterp --disable-tclinterp \
  --with-tlib=ncurses --enable-gui=no --disable-gpm --exec-prefix=/ \
  --with-compiledby="<bugzilla@redhat.com>" \
  --with-modified-by="<bugzilla@redhat.com>"

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/{after,autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/after/{autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
cp -f %{SOURCE11} .
%if %{?fedora}%{!?fedora:0} >= 16 || %{?rhel}%{!?rhel:0} >= 6
cp -f %{SOURCE15} $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/template.spec
%else
cp -f %{SOURCE14} $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/template.spec
%endif
cp runtime/doc/uganda.txt LICENSE
# Those aren't Linux info files but some binary files for Amiga:
rm -f README*.info


cd src
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
make installgtutorbin  DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m755 vim $RPM_BUILD_ROOT%{_bindir}/vi
install -m755 enhanced-vim $RPM_BUILD_ROOT%{_bindir}/vim
install -m755 gvim $RPM_BUILD_ROOT%{_bindir}/gvim
install -p -m644 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/gvim.png
install -p -m644 %{SOURCE8} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/gvim.png
install -p -m644 %{SOURCE9} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/gvim.png
install -p -m644 %{SOURCE10} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/gvim.png

( cd $RPM_BUILD_ROOT
  ln -sf vi ./%{_bindir}/rvi
  ln -sf vi ./%{_bindir}/rview
  ln -sf vi ./%{_bindir}/view
  ln -sf vi ./%{_bindir}/ex
  ln -sf vim ./%{_bindir}/rvim
  ln -sf vim ./%{_bindir}/vimdiff
  perl -pi -e "s,$RPM_BUILD_ROOT,," .%{_mandir}/man1/vim.1 .%{_mandir}/man1/vimtutor.1
  rm -f .%{_mandir}/man1/rvim.1
  ln -sf vim.1.gz .%{_mandir}/man1/vi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/rvi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/vimdiff.1.gz
  ln -sf gvim ./%{_bindir}/gview
  ln -sf gvim ./%{_bindir}/gex
  ln -sf gvim ./%{_bindir}/evim
  ln -sf gvim ./%{_bindir}/gvimdiff
  ln -sf gvim ./%{_bindir}/vimx
  %if "%{desktop_file}" == "1"
    mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
    desktop-file-install \
    %if 0%{?fedora} && 0%{?fedora} < 19
        --vendor fedora \
    %endif
        --dir $RPM_BUILD_ROOT/%{_datadir}/applications \
        %{SOURCE3}
        # --add-category "Development;TextEditor;X-Red-Hat-Base" D\
  %else
    mkdir -p ./%{_sysconfdir}/X11/applnk/Applications
    cp %{SOURCE3} ./%{_sysconfdir}/X11/applnk/Applications/gvim.desktop
  %endif
  # ja_JP.ujis is obsolete, ja_JP.eucJP is recommended.
  ( cd ./%{_datadir}/%{name}/%{vimdir}/lang; \
    ln -sf menu_ja_jp.ujis.vim menu_ja_jp.eucjp.vim )
)

pushd $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/tutor
mkdir conv
   iconv -f CP1252 -t UTF8 tutor.ca > conv/tutor.ca
   iconv -f CP1252 -t UTF8 tutor.it > conv/tutor.it
   #iconv -f CP1253 -t UTF8 tutor.gr > conv/tutor.gr
   iconv -f CP1252 -t UTF8 tutor.fr > conv/tutor.fr
   iconv -f CP1252 -t UTF8 tutor.es > conv/tutor.es
   iconv -f CP1252 -t UTF8 tutor.de > conv/tutor.de
   #iconv -f CP737 -t UTF8 tutor.gr.cp737 > conv/tutor.gr.cp737
   #iconv -f EUC-JP -t UTF8 tutor.ja.euc > conv/tutor.ja.euc
   #iconv -f SJIS -t UTF8 tutor.ja.sjis > conv/tutor.ja.sjis
   iconv -f UTF8 -t UTF8 tutor.ja.utf-8 > conv/tutor.ja.utf-8
   iconv -f UTF8 -t UTF8 tutor.ko.utf-8 > conv/tutor.ko.utf-8
   iconv -f CP1252 -t UTF8 tutor.no > conv/tutor.no
   iconv -f ISO-8859-2 -t UTF8 tutor.pl > conv/tutor.pl
   iconv -f ISO-8859-2 -t UTF8 tutor.sk > conv/tutor.sk
   iconv -f KOI8R -t UTF8 tutor.ru > conv/tutor.ru
   iconv -f CP1252 -t UTF8 tutor.sv > conv/tutor.sv
   mv -f tutor.ja.euc tutor.ja.sjis tutor.ko.euc tutor.pl.cp1250 tutor.zh.big5 tutor.ru.cp1251 tutor.zh.euc conv/
   rm -f tutor.ca tutor.de tutor.es tutor.fr tutor.gr tutor.it tutor.ja.utf-8 tutor.ko.utf-8 tutor.no tutor.pl tutor.sk tutor.ru tutor.sv
mv -f conv/* .
rmdir conv
popd

# Dependency cleanups
chmod 644 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/doc/vim2html.pl \
 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/tools/*.pl \
 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/tools/vim132
chmod 644 ../runtime/doc/vim2html.pl

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
  [ -x /%{_bindir}/id ] || return
  # [ \`/%{_bindir}/id -u\` -le 200 ] && return
  # for bash and zsh, only if no alias is already set
  alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.csh <<EOF
[ -x /%{_bindir}/id ] || exit
[ \`/%{_bindir}/id -u\` -gt 200 ] && alias vi vim
EOF
chmod 0644 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/*
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/vimrc
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/virc
(cd $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/doc;
 gzip -9 *.txt
 gzip -d help.txt.gz version7.txt.gz sponsor.txt.gz
 cp %{SOURCE12} .
 cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/;s/\tversion7.txt.gz\t/\tversion7.txt\t/;s/\tsponsor.txt.gz\t/\tsponsor.txt\t/' > tags.new; mv -f tags.new tags
cat >> tags << EOF
vi_help.txt	vi_help.txt	/*vi_help.txt*
vi-author.txt	vi_help.txt	/*vi-author*
vi-Bram.txt	vi_help.txt	/*vi-Bram*
vi-Moolenaar.txt	vi_help.txt	/*vi-Moolenaar*
vi-credits.txt	vi_help.txt	/*vi-credits*
EOF
LANG=C sort tags > tags.tmp; mv tags.tmp tags
 )
(cd ../runtime; rm -rf doc; ln -svf ../../vim/%{vimdir}/doc docs;) 
rm -f $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/tools
rm -rf $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~
( cd $RPM_BUILD_ROOT/%{_mandir}
  for i in `find ??/ -type f`; do
    bi=`basename $i`
    iconv -f latin1 -t UTF8 $i > $RPM_BUILD_ROOT/$bi
    mv -f $RPM_BUILD_ROOT/$bi $i
  done
)

# Remove not UTF-8 manpages
for i in pl.ISO8859-2 it.ISO8859-1 ru.KOI8-R fr.ISO8859-1; do
  rm -rf $RPM_BUILD_ROOT/%{_mandir}/$i
done

# use common man1/ru directory
mv $RPM_BUILD_ROOT/%{_mandir}/ru.UTF-8 $RPM_BUILD_ROOT/%{_mandir}/ru

# Remove duplicate man pages
for i in fr.UTF-8 it.UTF-8 pl.UTF-8; do
  rm -rf $RPM_BUILD_ROOT/%{_mandir}/$i
done

for i in rvim.1 gvim.1 gvimdiff.1; do 
  echo ".so man1/vim.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/$i
done
touch $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/doc/tags

%post X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /%{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi
update-desktop-database &> /dev/null ||:

%postun X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /%{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi
update-desktop-database &> /dev/null ||:

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/vimrc
%doc README* LICENSE 
%doc runtime/docs
%doc Changelog.rpm
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/vimfiles/template.spec
%dir %{_datadir}/%{name}/%{vimdir}
%{_datadir}/%{name}/%{vimdir}/autoload
%{_datadir}/%{name}/%{vimdir}/colors
%{_datadir}/%{name}/%{vimdir}/compiler
%{_datadir}/%{name}/%{vimdir}/doc
%{_datadir}/%{name}/%{vimdir}/*.vim
%{_datadir}/%{name}/%{vimdir}/ftplugin
%{_datadir}/%{name}/%{vimdir}/indent
%{_datadir}/%{name}/%{vimdir}/keymap
%{_datadir}/%{name}/%{vimdir}/lang/*.vim
%{_datadir}/%{name}/%{vimdir}/lang/*.txt
%dir %{_datadir}/%{name}/%{vimdir}/lang
%{_datadir}/%{name}/%{vimdir}/macros
%{_datadir}/%{name}/%{vimdir}/plugin
%{_datadir}/%{name}/%{vimdir}/print
%{_datadir}/%{name}/%{vimdir}/syntax
%{_datadir}/%{name}/%{vimdir}/tutor
%if ! %{withvimspell}
%{_datadir}/%{name}/%{vimdir}/spell
%endif
%lang(af) %{_datadir}/%{name}/%{vimdir}/lang/af
%lang(ca) %{_datadir}/%{name}/%{vimdir}/lang/ca
%lang(cs) %{_datadir}/%{name}/%{vimdir}/lang/cs
%lang(cs.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/cs.cp1250
%lang(de) %{_datadir}/%{name}/%{vimdir}/lang/de
%lang(en_GB) %{_datadir}/%{name}/%{vimdir}/lang/en_GB
%lang(eo) %{_datadir}/%{name}/%{vimdir}/lang/eo
%lang(es) %{_datadir}/%{name}/%{vimdir}/lang/es
%lang(fi) %{_datadir}/%{name}/%{vimdir}/lang/fi
%lang(fr) %{_datadir}/%{name}/%{vimdir}/lang/fr
%lang(ga) %{_datadir}/%{name}/%{vimdir}/lang/ga
%lang(it) %{_datadir}/%{name}/%{vimdir}/lang/it
%lang(ja) %{_datadir}/%{name}/%{vimdir}/lang/ja
%lang(ja.sjis) %{_datadir}/%{name}/%{vimdir}/lang/ja.sjis
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko.UTF-8
%lang(nb) %{_datadir}/%{name}/%{vimdir}/lang/nb
%lang(nl) %{_datadir}/%{name}/%{vimdir}/lang/nl
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/no
%lang(pl) %{_datadir}/%{name}/%{vimdir}/lang/pl
%lang(pl.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/pl.UTF-8
%lang(pl.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/pl.cp1250
%lang(pt_BR) %{_datadir}/%{name}/%{vimdir}/lang/pt_BR
%lang(ru) %{_datadir}/%{name}/%{vimdir}/lang/ru
%lang(ru.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/ru.cp1251
%lang(sk) %{_datadir}/%{name}/%{vimdir}/lang/sk
%lang(sk.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/sk.cp1250
%lang(sv) %{_datadir}/%{name}/%{vimdir}/lang/sv
%lang(uk) %{_datadir}/%{name}/%{vimdir}/lang/uk
%lang(uk.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/uk.cp1251
%lang(vi) %{_datadir}/%{name}/%{vimdir}/lang/vi
%lang(zh_CN) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN
%lang(zh_CN.cp936) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.cp936
%lang(zh_TW) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW.UTF-8
/%{_bindir}/xxd
%{_mandir}/man1/vim.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/view.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/xxd.*
%lang(fr) %{_mandir}/fr/man1/*
%lang(it) %{_mandir}/it/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(ru) %{_mandir}/ru/man1/*

%if %{withvimspell}
%files spell
%defattr(-,root,root)
%dir %{_datadir}/%{name}/%{vimdir}/spell
%{_datadir}/%{name}/vim70/spell/cleanadd.vim
%lang(af) %{_datadir}/%{name}/%{vimdir}/spell/af.*
%lang(am) %{_datadir}/%{name}/%{vimdir}/spell/am.*
%lang(bg) %{_datadir}/%{name}/%{vimdir}/spell/bg.*
%lang(ca) %{_datadir}/%{name}/%{vimdir}/spell/ca.*
%lang(cs) %{_datadir}/%{name}/%{vimdir}/spell/cs.*
%lang(cy) %{_datadir}/%{name}/%{vimdir}/spell/cy.*
%lang(da) %{_datadir}/%{name}/%{vimdir}/spell/da.*
%lang(de) %{_datadir}/%{name}/%{vimdir}/spell/de.*
%lang(el) %{_datadir}/%{name}/%{vimdir}/spell/el.*
%lang(en) %{_datadir}/%{name}/%{vimdir}/spell/en.*
%lang(eo) %{_datadir}/%{name}/%{vimdir}/spell/eo.*
%lang(es) %{_datadir}/%{name}/%{vimdir}/spell/es.*
%lang(fo) %{_datadir}/%{name}/%{vimdir}/spell/fo.*
%lang(fr) %{_datadir}/%{name}/%{vimdir}/spell/fr.*
%lang(ga) %{_datadir}/%{name}/%{vimdir}/spell/ga.*
%lang(gd) %{_datadir}/%{name}/%{vimdir}/spell/gd.*
%lang(gl) %{_datadir}/%{name}/%{vimdir}/spell/gl.*
%lang(he) %{_datadir}/%{name}/%{vimdir}/spell/he.*
%lang(hr) %{_datadir}/%{name}/%{vimdir}/spell/hr.*
%lang(hu) %{_datadir}/%{name}/%{vimdir}/spell/hu.*
%lang(id) %{_datadir}/%{name}/%{vimdir}/spell/id.*
%lang(it) %{_datadir}/%{name}/%{vimdir}/spell/it.*
%lang(ku) %{_datadir}/%{name}/%{vimdir}/spell/ku.*
%lang(la) %{_datadir}/%{name}/%{vimdir}/spell/la.*
%lang(lt) %{_datadir}/%{name}/%{vimdir}/spell/lt.*
%lang(lv) %{_datadir}/%{name}/%{vimdir}/spell/lv.*
%lang(mg) %{_datadir}/%{name}/%{vimdir}/spell/mg.*
%lang(mi) %{_datadir}/%{name}/%{vimdir}/spell/mi.*
%lang(ms) %{_datadir}/%{name}/%{vimdir}/spell/ms.*
%lang(nb) %{_datadir}/%{name}/%{vimdir}/spell/nb.*
%lang(nl) %{_datadir}/%{name}/%{vimdir}/spell/nl.*
%lang(nn) %{_datadir}/%{name}/%{vimdir}/spell/nn.*
%lang(ny) %{_datadir}/%{name}/%{vimdir}/spell/ny.*
%lang(pl) %{_datadir}/%{name}/%{vimdir}/spell/pl.*
%lang(pt) %{_datadir}/%{name}/%{vimdir}/spell/pt.*
%lang(ro) %{_datadir}/%{name}/%{vimdir}/spell/ro.*
%lang(ru) %{_datadir}/%{name}/%{vimdir}/spell/ru.*
%lang(rw) %{_datadir}/%{name}/%{vimdir}/spell/rw.*
%lang(sk) %{_datadir}/%{name}/%{vimdir}/spell/sk.*
%lang(sl) %{_datadir}/%{name}/%{vimdir}/spell/sl.*
%lang(sv) %{_datadir}/%{name}/%{vimdir}/spell/sv.*
%lang(sw) %{_datadir}/%{name}/%{vimdir}/spell/sw.*
%lang(tet) %{_datadir}/%{name}/%{vimdir}/spell/tet.*
%lang(th) %{_datadir}/%{name}/%{vimdir}/spell/th.*
%lang(tl) %{_datadir}/%{name}/%{vimdir}/spell/tl.*
%lang(tn) %{_datadir}/%{name}/%{vimdir}/spell/tn.*
%lang(uk) %{_datadir}/%{name}/%{vimdir}/spell/uk.*
%lang(yi) %{_datadir}/%{name}/%{vimdir}/spell/yi.*
%lang(yi-tr) %{_datadir}/%{name}/%{vimdir}/spell/yi-tr.*
%lang(zu) %{_datadir}/%{name}/%{vimdir}/spell/zu.*
%endif

%files minimal
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/virc
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvi
%{_bindir}/rview

%files enhanced
%defattr(-,root,root)
%{_bindir}/vim
%{_bindir}/rvim
%{_bindir}/vimdiff
%{_bindir}/vimtutor
%config(noreplace) %{_sysconfdir}/profile.d/vim.*
%{_mandir}/man1/rvim.*
%{_mandir}/man1/vimdiff.*
%{_mandir}/man1/vimtutor.*

%files filesystem
%defattr(-,root,root)
%dir %{_datadir}/%{name}/vimfiles
%dir %{_datadir}/%{name}/vimfiles/after
%dir %{_datadir}/%{name}/vimfiles/after/*
%dir %{_datadir}/%{name}/vimfiles/autoload
%dir %{_datadir}/%{name}/vimfiles/colors
%dir %{_datadir}/%{name}/vimfiles/compiler
%dir %{_datadir}/%{name}/vimfiles/doc
%ghost %{_datadir}/%{name}/vimfiles/doc/tags
%dir %{_datadir}/%{name}/vimfiles/ftdetect
%dir %{_datadir}/%{name}/vimfiles/ftplugin
%dir %{_datadir}/%{name}/vimfiles/indent
%dir %{_datadir}/%{name}/vimfiles/keymap
%dir %{_datadir}/%{name}/vimfiles/lang
%dir %{_datadir}/%{name}/vimfiles/plugin
%dir %{_datadir}/%{name}/vimfiles/print
%dir %{_datadir}/%{name}/vimfiles/spell
%dir %{_datadir}/%{name}/vimfiles/syntax
%dir %{_datadir}/%{name}/vimfiles/tutor

%files X11
%defattr(-,root,root)
%if "%{desktop_file}" == "1"
/%{_datadir}/applications/*
%else
/%{_sysconfdir}/X11/applnk/*/gvim.desktop
%endif
%{_bindir}/gvimtutor
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/gview
%{_bindir}/gex
%{_bindir}/vimx
%{_bindir}/evim
%{_mandir}/man1/evim.*
%{_mandir}/man1/gvim*
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Mon Feb 18 2013 Karsten Hopp <karsten@redhat.com> 7.3.822-1
- patchlevel 822

* Fri Feb 15 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 7.3.797-2
- Only use --vendor for desktop-file-install on F18 or less

* Thu Jan 31 2013 Karsten Hopp <karsten@redhat.com> 7.3.797-1
- patchlevel 797

* Mon Jan 28 2013 Karsten Hopp <karsten@redhat.com> 7.3.785-1
- patchlevel 785

* Tue Nov 20 2012 Karsten Hopp <karsten@redhat.com> 7.3.715-1
- patchlevel 715

* Tue Oct 23 2012 Karsten Hopp <karsten@redhat.com> 7.3.712-1
- patchlevel 712

* Mon Oct 15 2012 Karsten Hopp <karsten@redhat.com> 7.3.691-1
- patchlevel 691

* Fri Oct 05 2012 Karsten Hopp <karsten@redhat.com> 7.3.682-1
- patchlevel 682
- use --enable-rubyinterp=dynamic and --enable-pythoninterp=dynamic

* Mon Sep 03 2012 Karsten Hopp <karsten@redhat.com> 7.3.646-1
- patchlevel 646

* Tue Aug 28 2012 Karsten Hopp <karsten@redhat.com> 7.3.638-2
- fix some man page typos (#668894, #675480)
- own usr/share/vim/vimfiles/doc/tags (#845564)
- add path to csope database (#844843)

* Tue Aug 28 2012 Karsten Hopp <karsten@redhat.com> 7.3.638-1
- patchlevel 638

* Mon Aug 06 2012 Karsten Hopp <karsten@redhat.com> 2:7.3.622-2
- add epoch to spec.vim and automatic changelog entries

* Mon Aug 06 2012 Karsten Hopp <karsten@redhat.com> 7.3.622-1
- patchlevel 622

* Mon Aug 06 2012 Karsten Hopp <karsten@redhat.com> 7.3.604-1
- drop vim-6.1-rh3.patch, (bz #754801)

* Wed Jul 18 2012 Karsten Hopp <karsten@redhat.com> 7.3.604-1
- patchlevel 604

* Wed Jul 11 2012 Petr Pisar <ppisar@redhat.com> - 2:7.3.594-2
- Perl 5.16 rebuild

* Tue Jul 10 2012 Karsten Hopp <karsten@redhat.com> 7.3.594-1
- patchlevel 594

* Tue Jul 10 2012 Karsten Hopp <karsten@redhat.com> 7.3.592-1
- patchlevel 592

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 2:7.3.584-2
- Perl 5.16 rebuild

* Mon Jul 02 2012 Karsten Hopp <karsten@redhat.com> 7.3.584-1
- patchlevel 584

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 2:7.3.556-2
- Perl 5.16 rebuild

* Mon Jun 18 2012 Karsten Hopp <karsten@redhat.com> 7.3.556-1
- patchlevel 556

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2:7.3.515-2
- Perl 5.16 rebuild

* Mon May 21 2012 Karsten Hopp <karsten@redhat.com> 7.3.515-1
- enable highlighting for older log files (#816848)

* Tue May 08 2012 Karsten Hopp <karsten@redhat.com> 7.3.515-1
- patchlevel 515

* Fri Mar 16 2012 Karsten Hopp <karsten@redhat.com> 7.3.471-1
- patchlevel 471

* Mon Feb 13 2012 Karsten Hopp <karsten@redhat.com> 7.3.444-1
- patchlevel 444

* Tue Feb 07 2012 Karsten Hopp <karsten@redhat.com> 7.3.434-1
- patchlevel 434

* Tue Feb 07 2012 Karsten Hopp <karsten@redhat.com> 7.3.393-3
- update spec file template, bugzilla 736774

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 7.3.393-3
- rebuild against the new ruby library

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 7.3.393-2
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Thu Jan 05 2012 Karsten Hopp <karsten@redhat.com> 7.3.393-1
- patchlevel 393
- fix boolean key 'Terminal' in gvim.desktop

* Fri Dec 23 2011 Karsten Hopp <karsten@redhat.com> 7.3.386-1
- patchlevel 386

* Mon Sep 26 2011 Karsten Hopp <karsten@redhat.com> 7.3.322-1
- patchlevel 322

* Wed Sep 21 2011 Karsten Hopp <karsten@redhat.com> 7.3.315-1
- patchlevel 315

* Mon Aug 29 2011 Karsten Hopp <karsten@redhat.com> 7.3.289-1
- patchlevel 289

* Mon Aug 29 2011 Karsten Hopp <karsten@redhat.com> 7.3.244-4
- Remove old patched files. (Ricky Zhou <ricky@fedoraproject.org>)
  (bugzilla #709456)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2:7.3.244-3
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2:7.3.244-2
- Perl mass rebuild

* Mon Jul 11 2011 Karsten Hopp <karsten@redhat.com> 7.3.244-1
- patchlevel 244

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2:7.3.206-3
- Perl mass rebuild

* Tue May 31 2011 Ville Skyttä <ville.skytta@iki.fi> - 2:7.3.206-2
- Own the /usr/share/vim/vim73 dir.

* Mon May 30 2011 Karsten Hopp <karsten@redhat.com> 7.3.206-1
- drop xxd-locale patch
- update to patchlevel 206

* Wed May 11 2011 Karsten Hopp <karsten@redhat.com> 7.3.189-1
- patchlevel 189

* Wed Mar 16 2011 Karsten Hopp <karsten@redhat.com> 7.3.138-1
- patchlevel 138

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.3.107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Karsten Hopp <karsten@redhat.com> 7.3.107-1
- patchlevel 107

* Mon Jan 10 2011 Karsten Hopp <karsten@redhat.com> 7.3.099-1
- patchlevel 099

* Mon Jan 03 2011 Karsten Hopp <karsten@redhat.com> 7.3.094-1
- patchlevel 094

* Thu Dec 09 2010 Karsten Hopp <karsten@redhat.com> 7.3.081-1
- patchlevel 081

* Wed Dec 08 2010 Karsten Hopp <karsten@redhat.com> 7.3.080-1
- patchlevel 080

* Fri Dec 03 2010 Karsten Hopp <karsten@redhat.com> 7.3.075-1
- patchlevel 075

* Thu Dec 02 2010 Karsten Hopp <karsten@redhat.com> 7.3.073-1
- patchlevel 073

* Thu Nov 25 2010 Karsten Hopp <karsten@redhat.com> 7.3.069-1
- patchlevel 069

* Wed Nov 24 2010 Karsten Hopp <karsten@redhat.com> 7.3.068-1
- patchlevel 068

* Wed Nov 24 2010 Karsten Hopp <karsten@redhat.com> 7.3.063-1
- patchlevel 063

* Wed Nov 17 2010 Karsten Hopp <karsten@redhat.com> 7.3.062-1
- patchlevel 062

* Tue Nov 16 2010 Karsten Hopp <karsten@redhat.com> 7.3.061-1
- patchlevel 061

* Tue Nov 16 2010 Karsten Hopp <karsten@redhat.com> 7.3.056-1
- patchlevel 056

* Thu Nov 11 2010 Karsten Hopp <karsten@redhat.com> 7.3.055-1
- patchlevel 055

* Wed Nov 10 2010 Karsten Hopp <karsten@redhat.com> 7.3.051-1
- patchlevel 051

* Thu Nov 04 2010 Karsten Hopp <karsten@redhat.com> 7.3.050-1
- patchlevel 050

* Thu Nov 04 2010 Karsten Hopp <karsten@redhat.com> 7.3.048-1
- patchlevel 048

* Thu Oct 28 2010 Karsten Hopp <karsten@redhat.com> 7.3.047-1
- patchlevel 047

* Wed Oct 27 2010 Karsten Hopp <karsten@redhat.com> 7.3.046-1
- patchlevel 046

* Wed Oct 27 2010 Karsten Hopp <karsten@redhat.com> 7.3.039-1
- patchlevel 039

* Sun Oct 24 2010 Karsten Hopp <karsten@redhat.com> 7.3.035-1
- patchlevel 035

* Sat Oct 23 2010 Karsten Hopp <karsten@redhat.com> 7.3.034-1
- patchlevel 034

* Sat Oct 23 2010 Karsten Hopp <karsten@redhat.com> 7.3.033-1
- patchlevel 033

* Thu Oct 21 2010 Karsten Hopp <karsten@redhat.com> 7.3.032-1
- patchlevel 032

* Wed Oct 20 2010 Karsten Hopp <karsten@redhat.com> 7.3.031-1
- patchlevel 031

* Sat Oct 16 2010 Karsten Hopp <karsten@redhat.com> 7.3.029-1
- patchlevel 029

* Fri Oct 15 2010 Karsten Hopp <karsten@redhat.com> 7.3.028-1
- patchlevel 028

* Thu Oct 14 2010 Karsten Hopp <karsten@redhat.com> 7.3.027-1
- patchlevel 027

* Wed Oct 13 2010 Karsten Hopp <karsten@redhat.com> 7.3.026-1
- patchlevel 026

* Sun Oct 10 2010 Karsten Hopp <karsten@redhat.com> 7.3.021-1
- patchlevel 021

* Sat Oct 09 2010 Karsten Hopp <karsten@redhat.com> 7.3.020-1
- patchlevel 020

* Fri Oct 01 2010 Karsten Hopp <karsten@redhat.com> 7.3.019-1
- patchlevel 019

* Thu Sep 30 2010 Karsten Hopp <karsten@redhat.com> 7.3.018-1
- patchlevel 018

* Thu Sep 30 2010 Karsten Hopp <karsten@redhat.com> 7.3.011-3
- add filesystem subpackage (#628293)

* Wed Sep 29 2010 jkeating - 2:7.3.011-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Karsten Hopp <karsten@redhat.com> 7.3.011-1
- update to VIM 7.3 patchlevel 011

# vim:nrformats-=octal
