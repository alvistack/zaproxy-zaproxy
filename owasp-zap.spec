# Copyright 2023 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
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
Version: 2.13.0
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

ZAP_DOWNLOAD_URL=http://github.com/zaproxy/zaproxy/releases/download/v2.13.0/ZAP_2.13.0_Linux.tar.gz
ZAP_DOWNLOAD_DEST=/tmp/ZAP_2.13.0_Linux.tar.gz
ZAP_DOWNLOAD_CHECKSUM=936eb52a0fd390c1ef890c455420d95ce20062fe136ec0927e023e2baf50f549

wget -c $ZAP_DOWNLOAD_URL -O $ZAP_DOWNLOAD_DEST
echo -n "$ZAP_DOWNLOAD_CHECKSUM $ZAP_DOWNLOAD_DEST" | sha256sum -c -

rm -rf /usr/share/owasp-zap
mkdir -p /usr/share/owasp-zap
tar zxf $ZAP_DOWNLOAD_DEST -C /usr/share/owasp-zap --strip-components=1

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
