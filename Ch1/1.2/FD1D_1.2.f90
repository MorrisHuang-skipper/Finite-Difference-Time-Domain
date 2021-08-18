!========================================================
!   Purpose: 1D FDTD simulation in free space with a 
!            Gaussian pulse at the center(soft source)
!            with absorbing boundary condition
!
!   Methods: 1D FDTD + absorbing boundary condition
!       
!       Date        Programer       Description of change
!       ====        =========       =====================
!      9/6/20        MorrisH        Original Code
!========================================================
PROGRAM main
    IMPLICIT NONE
    ! number of cells to be used
    REAL(8), PARAMETER :: pi = 3.14159
    INTEGER, PARAMETER :: Ncell = 200
    REAL(8) :: Ex(Ncell), Hy(Ncell)
    INTEGER :: k, kc, T
    REAL(8) :: t0, width, pulse
    REAL(8) :: Ex_low_m1 = 0, Ex_high_m1 = 0, &
               Ex_low_m2 = 0, Ex_high_m2 = 0
    REAL(8) :: freq_in, ddx, dt
    ! name of write file
    CHARACTER(len=15) :: str1
    CHARACTER(len=8) :: fmt
    fmt = '(I4.4)'

    ! initialize field
    Ex = 0.0
    Hy = 0.0
    ! center of the problem space
    kc = Ncell / 2
    ! center of the incident pulse
    t0 = 40.0
    ! width of the incident pulse
    width = 12
    
    freq_in = 700e6
    ddx = 0.01
    dt = ddx / 6e8
    
    steploop: do T = 0, 2000

        !!! START FDTD !!!
        ! calculate Ex-field
        Efield: do k = 2, Ncell
            Ex(k) = Ex(k) + 0.5 * (Hy(k-1) - Hy(k))
        end do Efield

        ! put gaussian pulse in the center
        ! pulse = exp(-0.5 * ((t0 - T) / width) ** 2.0)
        pulse = sin(2 * pi * freq_in * dt * T)
        Ex(150) = Ex(150) + pulse

        ! Absorbing Boundary Condition
        ! Ex(0)_n = Ex(1)_n-2
        Ex(1) = Ex_low_m2
        Ex_low_m2 = Ex_low_m1
        Ex_low_m1 = Ex(2)
        ! Ex(Ncell)_n = Ex(Ncell-1)_n-2
        Ex(Ncell) = Ex_high_m2
        Ex_high_m2 = Ex_high_m1
        Ex_high_m1 = Ex(Ncell-1)

        ! calculate Hy-field
        Hfield: do k = 1, Ncell-1
            Hy(k) = Hy(k) + 0.5 * (Ex(k) - Ex(k+1))
        end do Hfield
        !!! END FDTD !!!

        ! output Ex and Hy field
        write(str1, fmt) T
        open(1, file='field/Ex_Hy_'//trim(str1)//'.dat', &
             status='unknown')
        output: do k = 1, Ncell
            write(1, *) Ex(k), Hy(k)
        end do output
        close(1)

    end do steploop 
END PROGRAM main
