%global  qt_version 6.7.2

Name:          qt6-qtgraphs
Version: 6.7.2
Release:       0%{?dist}

Summary:       The Qt Graphs module enables you to visualize data in 3D
License:       BSD-3-Clause AND GFDL-1.3-no-invariants-only AND GPL-3.0-only
URL:           https://doc.qt.io/qt-6/qtgraphs-index.html
Source0:       %{name}-%{version}.tar.bz2

BuildRequires: clang
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qt6-qtbase-devel >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtquick3d-devel
BuildRequires: qt6-qtbase-private-devel

%description
The Qt Graphs module enables you to visualize data in 3D as bar,
scatter, and surface graphs. It's especially useful for visualizing
depth maps and large quantities of rapidly changing data, such as
data received from multiple sensors. The look and feel of graphs
can be customized by using themes or by adding custom items and labels.

Qt Graphs is built on Qt 6 and Qt Quick 3D to take advantage of
hardware acceleration and Qt Quick.

%package devel
Summary:       Development Files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF

%cmake_build

%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%files
%license LICENSES/BSD-3-Clause.txt LICENSES/GFDL*.txt LICENSES/GPL-*.txt
%{_qt6_libdir}/libQt6Graphs.so.6*
%{_qt6_libdir}/qt6/metatypes/qt6graphs_relwithdebinfo_metatypes.json
%{_qt6_libdir}/qt6/modules/Graphs.json
%{_qt6_qmldir}/QtGraphs

%files devel
%{_qt6_headerdir}/QtGraphs
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtGraphsTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Graphs
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6Graphsplugin*.cmake
%{_qt6_libdir}/libQt6Graphs.so
%{_qt6_libdir}/pkgconfig/Qt6Graphs.pc
%{_qt6_libdir}/libQt6Graphs.prl
%{_qt6_libdir}/qt6/mkspecs/modules/qt_lib_graphs*.pri
