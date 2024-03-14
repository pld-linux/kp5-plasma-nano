#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.27.10
%define		qtver		5.15.2
%define		kpname		plasma-nano
%define		kf5ver		5.39.0

Summary:	plasma-nano
Name:		kp5-%{kpname}
Version:	5.27.10
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	79ffc86387c7024bd834b349fba9b79f
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.0
BuildRequires:	Qt5Gui-devel >= 5.15.0
BuildRequires:	Qt5Network-devel >= 5.15.2
BuildRequires:	Qt5Qml-devel
BuildRequires:	Qt5Quick-devel
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf5-extra-cmake-modules >= 0.0.9
BuildRequires:	kf5-kwayland-devel >= 5.82
BuildRequires:	kf5-kwindowsystem-devel >= 5.82
BuildRequires:	kf5-plasma-framework-devel >= 5.82
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
A minimal plasma shell package intended for embedded devices.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%{_libdir}/qt5/qml/org/kde/plasma/private/nanoshell
%{_datadir}/metainfo/org.kde.plasma.nano.desktoptoolbox.appdata.xml
%{_datadir}/plasma/packages/org.kde.plasma.nano.desktoptoolbox
%{_datadir}/plasma/shells/org.kde.plasma.nano
%{_datadir}/kservices5/plasma-applet-org.kde.plasma.nano.desktop
%{_datadir}/kservices5/plasma-package-org.kde.plasma.nano.desktoptoolbox.desktop
