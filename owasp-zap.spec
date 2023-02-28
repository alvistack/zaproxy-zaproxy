# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global __strip /bin/true

%global __brp_mangle_shebangs /bin/true

Name: owasp-zap
Epoch: 100
Version: 2.12.0+20230227a61267da
Release: 1%{?dist}
BuildArch: noarch
Summary: Zed Attack Proxy
License: Apache-2.0
URL: https://github.com/zaproxy/zaproxy/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: -post-build-checks
Requires(pre): fdupes
Requires(pre): unzip
Requires(pre): wget

%description
The Zed Attack Proxy (ZAP) is an easy to use integrated penetration
testing tool for finding vulnerabilities in web applications. It is
designed to be used by people with a wide range of security experience
and as such is ideal for developers and functional testers who are new
to penetration testing. ZAP provides automated scanners as well as a set
of tools that allow you to find security vulnerabilities manually.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%install
install -Dpm755 -d %{buildroot}%{_datadir}/owasp-zap
install -Dpm755 -d %{buildroot}%{_datadir}/applications
install -Dpm644 -t %{buildroot}%{_datadir}/applications owasp-zap.desktop

%check

%post
set -euxo pipefail

ZAP_DOWNLOAD_URL=http://github.com/zaproxy/zaproxy/releases/download/w2023-02-27/ZAP_WEEKLY_D-2023-02-27.zip
ZAP_DOWNLOAD_DEST=/tmp/ZAP_WEEKLY_D-2023-02-27.zip
ZAP_DOWNLOAD_CHECKSUM=6bc3f726ca1d8cf7b3527718f1460586c1b7def15b1a9e1d238e5af6aab1fa23

wget -c $ZAP_DOWNLOAD_URL -O $ZAP_DOWNLOAD_DEST
echo -n "$ZAP_DOWNLOAD_CHECKSUM $ZAP_DOWNLOAD_DEST" | sha256sum -c -

mkdir -p /usr/share/owasp-zap
find /usr/share/owasp-zap -mindepth 1 | xargs rm -rf || echo $?
TMP_DIR="$(mktemp -d)" && \
    unzip -qq -d $TMP_DIR $ZAP_DOWNLOAD_DEST && \
    cp -rfT $TMP_DIR/* /usr/share/owasp-zap && \
    rm -rf $TMP_DIR

chmod a+x /usr/share/owasp-zap/zap.sh
pushd /usr/bin && \
    ln -fs /usr/share/owasp-zap/zap.sh owasp-zap && \
    popd
fdupes -qnrps /usr/share/owasp-zap

%files
%license LICENSE
%dir %{_datadir}/owasp-zap
%{_datadir}/applications/owasp-zap.desktop

%changelog
