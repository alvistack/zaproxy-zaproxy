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
Version: 2.11.1
Release: 1%{?dist}
BuildArch: noarch
Summary: DZed Attack Proxyependency Manager for PHP
License: Apache-2.0
URL: https://github.com/owasp-zap/owasp-zap/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: fdupes
Requires: java

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
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_datadir}/owasp-zap
install -Dpm755 -d %{buildroot}%{_datadir}/applications
cp -rfT owasp-zap %{buildroot}%{_datadir}/owasp-zap
install -Dpm644 -t %{buildroot}%{_datadir}/applications owasp-zap.desktop
pushd %{buildroot}%{_bindir} && \
    ln -fs %{_datadir}/owasp-zap/zap.sh owasp-zap && \
    popd
chmod a+x %{buildroot}%{_datadir}/owasp-zap/zap.sh
fdupes -qnrps %{buildroot}%{_datadir}/owasp-zap

%check

%files
%license LICENSE
%dir %{_datadir}/owasp-zap
%{_bindir}/*
%{_datadir}/owasp-zap/*
%{_datadir}/applications/owasp-zap.desktop

%changelog
