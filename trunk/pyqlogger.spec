# $Id$
%define _name           pyqlogger
%define _version        1.3.1
%define _rel            1
%define _prefix         /usr
%define _release        %_rel

Summary:                PyQT Blogger Client
Name:                   %{_name}
Version:                %{_version}
Release:                %{_release}
Source:                 http://download.berlios.de/pyqlogger/PyQLogger-%{_version}.tar.gz
URL:                    http://pyqlogger.berlios.de/
Group:                  Productivity/Networking/Blogging
Packager:               Xander Soldaat
License:                GPL
BuildRoot:              %{_tmppath}/build-%{_name}-%{_version}
Requires:               python-osd
Prefix:                 %{_prefix}
BuildArch:              noarch

%description
PyQLogger - PyQT Blogger Client by Reflog

Features:
- Simple and easy GUI
- Easy setup wizard
- Posts fetching from the blog for later editing and re-publishing
- Async and responsive UI
- Posts saving feature (drafts)
- On-Screen notifications of events
- Post editor with syntax highlighting
- Multiple blog support
- Post export
- Update notification (for pyqlogger itself)
- Pluggable features, like SpellChecker and others
- Unicode support
- Multiple blog providers

%prep
%setup -q -n "PyQLogger-%{_version}"

%build
python ./setup.py build

%install
%{__rm} -rf %{buildroot}
python ./setup.py install --root "${RPM_BUILD_ROOT}" --record=INSTALLED_FILES

%clean
%{__rm} -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc CHANGES.txt LICENSE.txt README.txt

%changelog
* Sun Dec  5 2004 Xander Soldaat <mightor@gmail.com>
- Initial release, spec file based on Pascal Bleser's src.rpm
